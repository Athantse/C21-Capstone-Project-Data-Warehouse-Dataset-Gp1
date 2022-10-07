from pyspark.sql import SparkSession
from datetime import datetime, date
from pyspark.sql import Row
from pyspark.sql.functions import udf
from pyspark.accumulators import AccumulatorParam
from dotenv import load_dotenv
import os

load_dotenv()

SPARK_MASTER = os.getenv('SPARK_MASTER')
RDS_HOST = os.getenv('RDS_HOST')
RDS_POSTGRES_DB = os.getenv('RDS_POSTGRES_DB')
RDS_POSTGRES_USER = os.getenv('RDS_POSTGRES_USER')
RDS_POSTGRES_PASSWORD = os.getenv('RDS_POSTGRES_PASSWORD')

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')


class DictAccumulatorParam(AccumulatorParam):
  def zero(self, value):
    return {}

  def addInPlace(self, v1, v2):
    v1.update(v2)
    return v1
    
global all_dates
all_dates = {}
global spark

def prepare_spark():
  packages = [
    "org.postgresql:postgresql:42.2.18"
  ]

  # .master('spark://{}:7077'.format(config.SPARK_MASTER))\
  spark = SparkSession.builder.appName("capstone ETL")\
      .master('spark://{}:7077'.format(SPARK_MASTER))\
      .config("spark.jars.packages",",".join(packages))\
      .getOrCreate()
  return spark

spark = prepare_spark()
# all_dates = spark.sparkContext.accumulator({}, DictAccumulatorParam())

def save_table(data_frame, table):
  data_frame.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://{}/{}".format(RDS_HOST,RDS_POSTGRES_DB)) \
    .option("driver",'org.postgresql.Driver')\
    .option("dbtable", table) \
    .option("user", RDS_POSTGRES_USER) \
    .option("password", RDS_POSTGRES_PASSWORD)\
    .mode("overwrite")\
    .save()
  data_frame.show(2)


def load_table(table):
  df = spark.read.parquet("/tmp/result/%s" % table)
  show_shape(df)


def load_psql_df(table):
  return spark.read.format('jdbc').options(
    url = "jdbc:postgresql://{}/{}".format(POSTGRES_HOST,POSTGRES_DB),
    user = POSTGRES_USER,
    password = POSTGRES_PASSWORD,
    dbtable = table,
    driver = "org.postgresql.Driver",
  ).load()


def show_shape(self):
  print("Rows: %d, Cols: %d" % (self.count(), len(self.columns)))
  print(self.columns)
  

def process_table(table):
  df = load_psql_df(table)
  dim_table = f"dim_{table}"
  save_table(df, dim_table)
  show_shape(df)

def gen_users():
  df = load_psql_df("users")
  df = df.select(
    "id",
    "birthday",
    "gender",
    "profession",
    "chronic_condition",
    "education",
  )

  df2 = df.withColumnRenamed("gender", "gender_id")\
          .withColumnRenamed("profession", "profession_id")\
          .withColumnRenamed("chronic_condition", "chronic_condition_id")\
          .withColumnRenamed("education", "education_id")
    
  save_table(df2, "dim_users")
  show_shape(df2)

from pyspark.sql.functions import col, lit

def gen_food():
  df = load_psql_df("food")
  df = df.select(
    "id",
    "food_name",
    lit('100g').alias("unit_of_food"),
    col("group_id").alias("food_group_id"),
    "food_calories",
    lit('kcal').alias("unit_of_calories"),
    "carbohydrates",
    "sugars",
    "fat",
    "protein",
    "fiber",
    "sodium",
  )
  save_table(df, "dim_food")
  show_shape(df)

def gen_excercise_types():
  df = load_psql_df("exercises_types")
  df = df.withColumn("unit_of_ex_calories", lit("kcal"))
  save_table(df, "dim_exercises_types")
  show_shape(df)

dim_tables = [
  'users',
  'gender',
  'profession_types',
  'diets_types',
  'chronic_condition',
  'education',
  'food',
  'food_groups',
  'exercises_types',
]

fact_tables = [
  'users_weight',
  'users_exercises',
  # 'users_diets_stats',
  # 'users_bg_stats',
  # 'users_bp_stats',
],

custom_tables = [
  'users_diets_stats',
  'users_bg_stats',
  'users_bp_stats',
]

def add_date(date):
  if date in all_dates:
    return all_dates[date]

  print("Date: %s" % date)
  date_id = len(all_dates) + 1
  all_dates[date] = date_id

  return date_id

@udf
def get_date_id(date):
  if date in all_dates:
    return all_dates[date]

  return 0

def gen_with_sql(intable, outtable, select):
  df = load_psql_df(intable)

  for row in df.select("date").collect():
    add_date(row[0])

  df = df.withColumn('date_id', get_date_id("date"))\
    .withColumn("date_id",col("date_id").cast("integer"))

  # df.show(5)

  view_name = "%s_view" % intable
  df.createOrReplaceTempView(view_name)
  stats_df = spark.sql("select %s from %s" % (select, view_name))

  save_table(stats_df, outtable)

def gen_dim_tables():
  for dim in dim_tables:
    process_table(dim)
  
def gen_fact_tables():
  gen_with_sql(
    "users_diets", "fact_users_diets_stats",
    "id, diet_type as diet_type_id, "
    "food as food_id, food_amount,"
    "'100g' as unit_of_food,"
    "date_id, user_id"
  )

  gen_with_sql(
    "users_weight", "fact_users_weight",
    "id, weight, date_id, user_id"
  )

  gen_with_sql(
    "users_exercises", "fact_users_exercises",
    "id, date_id, exercise as exercise_type_id," 
    "duration, user_id "
  )

  gen_with_sql(
    'users_blood_pressure', 'fact_users_bp_stats',
    "id, sys_bp, dia_bp, date_id, user_id"
  )

  gen_with_sql(
    'users_blood_glucose', 'fact_users_bg_stats',
    "id, bg_measurement, date_id, user_id"
  )

def split_date(id, date):
  # print("Date: %s" % date)
  return (id, date.year, date.month, date.day, 0)
  
def gen_date_table():
  data = []
  columns = ["id", "year", "month", "day", "hour"]

  for date, id in all_dates.items():
    data.append(split_date(id, date))

  print(data)
  df = spark.createDataFrame(data = data, schema = columns)
  save_table(df, "dim_date")

def main():
  gen_dim_tables()
  gen_fact_tables()
  gen_date_table()
  gen_users()
  gen_food()
  gen_excercise_types()

  print("All Date: %s" % all_dates)

if __name__ == "__main__":
  main()

