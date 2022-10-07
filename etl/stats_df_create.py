from datetime import datetime
import os
from site import USER_SITE
import install
from config import Config
config = Config()
from pyspark.sql import DataFrameReader
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DecimalType, FloatType
from pyspark.sql.types import StructType
from pyspark.sql.functions import col


def prepare_spark(config: Config):
    from pyspark.sql import SparkSession
    packages = [
        "com.amazonaws:aws-java-sdk-s3:1.12.95",
        "org.apache.hadoop:hadoop-aws:3.2.0",
        "org.apache.spark:spark-avro_2.12:3.3.0",
        "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1",
        "org.postgresql:postgresql:42.2.18"
    ]
    spark = SparkSession.builder.appName("Transform Recent change stream")\
        .master('spark://{}:7077'.format(config.SPARK_MASTER))\
        .config("spark.jars.packages",",".join(packages))\
        .config("spark.hadoop.fs.s3a.access.key",config.AWS_ACCESS_KEY)\
        .config("spark.hadoop.fs.s3a.secret.key",config.AWS_SECRET_KEY)\
        .config("spark.hadoop.fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")\
        .config('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')\
        .config("spark.hadoop.fs.s3a.multipart.size",104857600)\
        .config("com.amazonaws.services.s3a.enableV4", "true")\
        .config("spark.hadoop.fs.s3a.path.style.access", "false")\
        .getOrCreate()
    return spark

def process_data(spark, config, table):

    # read postgres data file

    df = spark.read.format('jdbc')\
            .option("url", "jdbc:postgresql://{}/{}".format(config.POSTGRES_HOST, config.POSTGRES_DB))\
            .option("dbtable", table)\
            .option("user", config.POSTGRES_USER)\
            .option("password", config.POSTGRES_PASSWORD)\
            .option("driver", "org.postgresql.Driver")\
            .load()
    return df

def save_data(df, table):
    df1 = df.write.format('jdbc')\
        .option("url", "jdbc:postgresql://{}/{}".format(config.RDS_POSTGRES_HOST, config.RDS_POSTGRES_DB))\
        .option("dbtable", table)\
        .option("user", config.RDS_POSTGRES_USER)\
        .option("password", config.RDS_POSTGRES_PASSWORD)\
        .option("driver", "org.postgresql.Driver")\
        .save()

def mancount(df):
    df.select()
    countman1 = df.filter(((df['birthday']) < '2020-12-31') & ((df['birthday']) > '2017-01-01') & (df['gender']==1)).count()
    countman2 = df.filter(((df['birthday']) < '2017-12-31') & ((df['birthday']) > '2011-01-01') & (df['gender']==1)).count()
    countman3 = df.filter(((df['birthday']) < '2011-12-31') & ((df['birthday']) > '2005-01-01') & (df['gender']==1)).count()
    countman4 = df.filter(((df['birthday']) < '2005-12-31') & ((df['birthday']) > '1958-01-01') & (df['gender']==1)).count()
    countman5 = df.filter(((df['birthday']) < '1958-12-31') & (df['gender']==1)).count()
    return countman1,countman2,countman3,countman4,countman5

def mancount_pf_el(df, data_type):
    df.select()
    pf_el_men_count1 = df.groupBy(data_type).count().orderBy(data_type, ascending=True)
    return pf_el_men_count1


def cal_food_calories (spark, user_id, countpeople, diet_type_id):
    dfusers_diets = process_data(spark,config,"users_diets")
    dffood = process_data(spark,config,"food")
    dates=[]
    calories_sum = 0
    for id in user_id:
        gropdiel = dfusers_diets.filter((dfusers_diets['user_id'] == id))
        rowsuserdiets = gropdiel.select('food','date','food_amount','diet_type').where(gropdiel['diet_type']== diet_type_id).collect()
        food_infos = [[rowsuserdiet.food, rowsuserdiet.food_amount,rowsuserdiet.date] for rowsuserdiet in rowsuserdiets]
        for food_info in food_infos:
            food = dffood.filter((dffood['id'] == food_info[0]))
            row_calories=food.select('food_calories').collect()
            foodCalories=[Calories.food_calories for Calories in row_calories]
            calories_sum +=(foodCalories[0]*food_info[1])
            dates.append(food_info[2])
    daycount=len(set(dates))
    avg_calories=calories_sum/(daycount*countpeople)
    return avg_calories

def nutrition_cal(spark, user_id, countpeople, nutrition_type):
    dfusers_diets = process_data(spark,config,"users_diets")
    dffood = process_data(spark,config,"food")
    dates=[]
    nutrition_sum = 0
    for id in user_id:
        gropdiel = dfusers_diets.filter((dfusers_diets['user_id'] == id))
        # gropdiel.show()
        rows_users_diets = gropdiel.select('food','date','food_amount').collect()
        nutrition_facts = [[row_user_diet.food, row_user_diet.food_amount,row_user_diet.date] for row_user_diet in rows_users_diets]
        for nutrition_fact in nutrition_facts:
            food = dffood.filter((dffood['id'] == nutrition_fact[0]))
            row_nutrition=food.select('{}'.format(nutrition_type)).collect()
            food_nutrition=[nutrition[nutrition_type] for nutrition in row_nutrition]
            nutrition_sum +=(food_nutrition[0]*nutrition_fact[1])
            dates.append(nutrition_fact[2])
    daycount=len(set(dates))
    avg_nutrition=nutrition_sum /(daycount * countpeople)
    return avg_nutrition


def ex_calories_cal (spark, usersId, countpeople):
    df_users_exercises = process_data(spark,config,"users_exercises")
    df_exercises_types = process_data(spark,config,"exercises_types")
    dates = []
    ex_calories_sum = 0

    for id in usersId:
        gropdiel = df_users_exercises.filter((df_users_exercises['user_id'] == id))
        rows_user_exs = gropdiel.select('exercise','date','duration').collect()
        ex_infos = [[rows_user_ex.exercise, rows_user_ex.duration, rows_user_ex.date] for rows_user_ex in rows_user_exs]
        for ex_info in ex_infos:
            ex = df_exercises_types.filter((df_exercises_types['id'] == ex_info[0]))
            row_ex_cal = ex.select('ex_calories').collect()
            ex_cal=[ex_calories.ex_calories for ex_calories in row_ex_cal]
            ex_calories_sum += (ex_cal[0] * ex_info[1])
            dates.append(ex_info[2])
    daycount=len(set(dates))
    avg_ex_cal=ex_calories_sum/(daycount * countpeople)
    return avg_ex_cal

def bg_cal (spark, users_id, countpeople):
    df_users_blood_glucose = process_data(spark, config, "users_blood_glucose")
    dates = []
    bg_sum = 0

    for id in users_id:
        gropdiel = df_users_blood_glucose.filter((df_users_blood_glucose['user_id'] == id))
        rows_users_bg = gropdiel.select('bg_measurement','date').collect()
        bg_infos = [[rows_user_bg.bg_measurement, rows_user_bg.date] for rows_user_bg in rows_users_bg]
        for bg_info in bg_infos:
            bg_sum += bg_info[0]
            dates.append(bg_info[1])
    daycount = len(set(dates))
    avg_bg = bg_sum / (daycount * countpeople)
    return avg_bg

def bp_cal (spark, users_id, countpeople):
    df_users_blood_pressure = process_data(spark, config, "users_blood_pressure")
    dates = []
    sys_bp_sum = 0
    dia_bp_sum = 0
    for id in users_id:
        print(id)
        gropdiel = df_users_blood_pressure.filter((df_users_blood_pressure['user_id'] == id))
        print(gropdiel)
        rows_users_bp = gropdiel.select('sys_bp', 'dia_bp', 'date').collect()
        print(rows_users_bp)
        bp_infos = [[rows_user_bp.sys_bp, rows_user_bp.dia_bp, rows_user_bp.date] for rows_user_bp in rows_users_bp]
        print(bp_infos)
        for bp_info in bp_infos:
            print(bp_info)
            sys_bp_sum += bp_info[0]
            print(sys_bp_sum)
            dia_bp_sum += bp_info[1]
            print(dia_bp_sum)
            dates.append(bp_info[2])
            print(dates)
    daycount = len(set(dates))
    print(daycount)
    avg_sys_bp = sys_bp_sum / (daycount * countpeople)
    avg_dia_bp = dia_bp_sum / (daycount * countpeople)
    print(avg_sys_bp)
    print(avg_dia_bp)
    return [avg_sys_bp, avg_dia_bp]



def cal_calories (spark, diet_type_id):
    dfusers = process_data(spark,config,"users")

    #  Group 1
    gropman1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender']==1))
    rowsuserman1 = gropman1.select('id').collect()
    valuemid1 = [row.id for row in rowsuserman1]
    group_men1_avg_calories = cal_food_calories(spark, valuemid1,gropman1.count(), diet_type_id)

    gropwomen1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen1 = gropwomen1.select('id').collect()
    valuewid1 = [row.id for row in rowsuserwomen1]
    group_women1_avg_calories=cal_food_calories(spark,valuewid1,gropwomen1.count(), diet_type_id)

    #  Group 2
    gropman2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender']==1))
    rowsuserman2 = gropman2.select('id').collect()
    valuemid2 = [row.id for row in rowsuserman2]
    group_men2_avg_calories = cal_food_calories(spark, valuemid2, gropman2.count(), diet_type_id)

    gropwomen2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender']==2))
    rowsuserwomen2 = gropwomen2.select('id').collect()
    valuewid2 = [row.id for row in rowsuserwomen2]
    group_women2_avg_calories = cal_food_calories(spark, valuewid2, gropwomen2.count(), diet_type_id)

    #  Group 3
    gropman3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender'] == 1))
    rowsuserman3 = gropman3.select('id').collect()
    valuemid3 = [row.id for row in rowsuserman3]
    group_men3_avg_calories = cal_food_calories(spark, valuemid3, gropman3.count(), diet_type_id)

    gropwomen3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen3 = gropwomen3.select('id').collect()
    valuewid3 = [row.id for row in rowsuserwomen3]
    group_women3_avg_calories = cal_food_calories(spark, valuewid3, gropwomen3.count(), diet_type_id)

    #  Group 4
    gropman4 = dfusers.filter( ((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender'] == 1))
    rowsuserman4 = gropman4.select('id').collect()
    valuemid4 = [row.id for row in rowsuserman4]
    group_men4_avg_calories = cal_food_calories(spark, valuemid4, gropman4.count(), diet_type_id)

    gropwomen4 = dfusers.filter(((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen4 = gropwomen4.select('id').collect()
    valuewid4 = [row.id for row in rowsuserwomen4]
    group_women4_avg_calories = cal_food_calories(spark, valuewid4, gropwomen4.count(), diet_type_id)

    #  Group 5
    gropman5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender'] == 1))
    rowsuserman5 = gropman5.select('id').collect()
    valuemid5 = [row.id for row in rowsuserman5]
    group_men5_avg_calories = cal_food_calories(spark, valuemid5, gropman5.count(), diet_type_id)

    gropwomen5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender'] == 2))
    rowsuserwomen5 = gropwomen5.select('id').collect()
    valuewid5 = [row.id for row in rowsuserwomen5]
    group_women5_avg_calories = cal_food_calories(spark, valuewid5, gropwomen5.count(), diet_type_id)

    input_schema = StructType(
        [
            StructField("ID", StringType(), True),
            StructField("age_group", StringType(), True),
            StructField("men_average_calories", DecimalType(), True),
            StructField("women_average_calories", DecimalType(), True),
        ])
    input_data = [
        ("1", "2-5歲", group_men1_avg_calories,group_women1_avg_calories),
        ("2", "6-11歲", group_men2_avg_calories,group_women2_avg_calories),
        ("3", "12-17歲", group_men3_avg_calories,group_women3_avg_calories),
        ("4", "18-64歲", group_men4_avg_calories,group_women4_avg_calories),
        ("5", "65歲以上", group_men5_avg_calories,group_women5_avg_calories),
    ]
    input_df = spark.createDataFrame(data=input_data, schema=input_schema)

    return input_df

def avg_nutrition_cal (spark, nutrition_type):
    dfusers = process_data(spark,config,"users")
    print(f'nutrition_type in line 215: {nutrition_type}')
    #  Group 1
    gropman1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender']==1))
    rowsuserman1 = gropman1.select('id').collect()
    valuemid1 = [row.id for row in rowsuserman1]
    group_men1_avg_calories = nutrition_cal(spark, valuemid1,gropman1.count(), nutrition_type)

    gropwomen1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen1 = gropwomen1.select('id').collect()
    valuewid1 = [row.id for row in rowsuserwomen1]
    group_women1_avg_calories = nutrition_cal(spark,valuewid1,gropwomen1.count(), nutrition_type)

    # #  Group 2
    gropman2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender_id']==1))
    rowsuserman2 = gropman2.select('id').collect()
    valuemid2 = [row.id for row in rowsuserman2]
    group_men2_avg_calories = nutrition_cal(spark, valuemid2, gropman2.count(), nutrition_type)

    gropwomen2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender_id']==2))
    rowsuserwomen2 = gropwomen2.select('id').collect()
    valuewid2 = [row.id for row in rowsuserwomen2]
    group_women2_avg_calories = nutrition_cal(spark, valuewid2, gropwomen2.count(), nutrition_type)

    # #  Group 3
    gropman3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender_id'] == 1))
    rowsuserman3 = gropman3.select('id').collect()
    valuemid3 = [row.id for row in rowsuserman3]
    group_men3_avg_calories = nutrition_cal(spark, valuemid3, gropman3.count(), nutrition_type)

    gropwomen3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender_id'] == 2))
    rowsuserwomen3 = gropwomen3.select('id').collect()
    valuewid3 = [row.id for row in rowsuserwomen3]
    group_women3_avg_calories = nutrition_cal(spark, valuewid3, gropwomen3.count(), nutrition_type)

    # #  Group 4
    gropman4 = dfusers.filter( ((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender_id'] == 1))
    rowsuserman4 = gropman4.select('id').collect()
    valuemid4 = [row.id for row in rowsuserman4]
    group_men4_avg_calories = nutrition_cal(spark, valuemid4, gropman4.count(), nutrition_type)

    gropwomen4 = dfusers.filter(((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender_id'] == 2))
    rowsuserwomen4 = gropwomen4.select('id').collect()
    valuewid4 = [row.id for row in rowsuserwomen4]
    group_women4_avg_calories = nutrition_cal(spark, valuewid4, gropwomen4.count(), nutrition_type)

    # #  Group 5
    gropman5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender_id'] == 1))
    rowsuserman5 = gropman5.select('id').collect()
    valuemid5 = [row.id for row in rowsuserman5]
    group_men5_avg_calories = nutrition_cal(spark, valuemid5, gropman5.count(), nutrition_type)

    gropwomen5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender_id'] == 2))
    rowsuserwomen5 = gropwomen5.select('id').collect()
    valuewid5 = [row.id for row in rowsuserwomen5]
    group_women5_avg_calories = nutrition_cal(spark, valuewid5, gropwomen5.count(), nutrition_type)

    input_schema = StructType(
        [
            StructField("ID", StringType(), True),
            StructField("age_group", StringType(), True),
            StructField("men_average_nutrition_intake", DecimalType(), True),
            StructField("women_average_nutrition_intake", DecimalType(), True),
        ])
    input_data = [
        ("1", "2-5歲", group_men1_avg_calories,group_women1_avg_calories),
        ("2", "6-11歲", group_men2_avg_calories,group_women2_avg_calories),
        ("3", "12-17歲", group_men3_avg_calories,group_women3_avg_calories),
        ("4", "18-65歲", group_men4_avg_calories,group_women4_avg_calories),
        ("5", "65歲以上", group_men5_avg_calories,group_women5_avg_calories),
    ]
    input_df = spark.createDataFrame(data=input_data, schema=input_schema)
    return input_df

def avg_ex_cal (spark):
    dfusers = process_data(spark,config,"users")
    #  Group 1
    gropman1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender']==1))
    rowsuserman1 = gropman1.select('id').collect()
    valuemid1 = [row.id for row in rowsuserman1]
    group_men1_avg_calories = ex_calories_cal(spark, valuemid1,gropman1.count())

    gropwomen1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen1 = gropwomen1.select('id').collect()
    valuewid1 = [row.id for row in rowsuserwomen1]
    group_women1_avg_calories = ex_calories_cal(spark,valuewid1,gropwomen1.count())

    #  Group 2
    gropman2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender']==1))
    rowsuserman2 = gropman2.select('id').collect()
    valuemid2 = [row.id for row in rowsuserman2]
    group_men2_avg_calories = ex_calories_cal(spark, valuemid2, gropman2.count())

    gropwomen2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender']==2))
    rowsuserwomen2 = gropwomen2.select('id').collect()
    valuewid2 = [row.id for row in rowsuserwomen2]
    group_women2_avg_calories = ex_calories_cal(spark, valuewid2, gropwomen2.count())

    #  Group 3
    gropman3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender'] == 1))
    rowsuserman3 = gropman3.select('id').collect()
    valuemid3 = [row.id for row in rowsuserman3]
    group_men3_avg_calories = ex_calories_cal(spark, valuemid3, gropman3.count())

    gropwomen3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen3 = gropwomen3.select('id').collect()
    valuewid3 = [row.id for row in rowsuserwomen3]
    group_women3_avg_calories = ex_calories_cal(spark, valuewid3, gropwomen3.count())

    #  Group 4
    gropman4 = dfusers.filter( ((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender'] == 1))
    rowsuserman4 = gropman4.select('id').collect()
    valuemid4 = [row.id for row in rowsuserman4]
    group_men4_avg_calories = ex_calories_cal(spark, valuemid4, gropman4.count())

    gropwomen4 = dfusers.filter(((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen4 = gropwomen4.select('id').collect()
    valuewid4 = [row.id for row in rowsuserwomen4]
    group_women4_avg_calories = ex_calories_cal(spark, valuewid4, gropwomen4.count()) 

    #  Group 5
    gropman5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender'] == 1))
    rowsuserman5 = gropman5.select('id').collect()
    valuemid5 = [row.id for row in rowsuserman5]
    group_men5_avg_calories = ex_calories_cal(spark, valuemid5, gropman5.count())

    gropwomen5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender'] == 2))
    rowsuserwomen5 = gropwomen5.select('id').collect()
    valuewid5 = [row.id for row in rowsuserwomen5]
    group_women5_avg_calories = ex_calories_cal(spark, valuewid5, gropwomen5.count())

    input_schema = StructType(
        [
            StructField("ID", StringType(), True),
            StructField("age_group", StringType(), True),
            StructField("men_average_ex_cal_burned", DecimalType(), True),
            StructField("women_average_ex_cal_burned", DecimalType(), True),
        ])
    input_data = [
        ("1", "2-5歲", group_men1_avg_calories,group_women1_avg_calories),
        ("2", "6-11歲", group_men2_avg_calories,group_women2_avg_calories),
        ("3", "12-17歲", group_men3_avg_calories,group_women3_avg_calories),
        ("4", "18-65歲", group_men4_avg_calories,group_women4_avg_calories),
        ("5", "65歲以上", group_men5_avg_calories,group_women5_avg_calories),
    ]
    input_df = spark.createDataFrame(data=input_data, schema=input_schema)
    return input_df


def avg_bg (spark):
    dfusers = process_data(spark,config,"users")
    #  Group 1
    gropman1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender']==1))
    rowsuserman1 = gropman1.select('id').collect()
    valuemid1 = [row.id for row in rowsuserman1]
    group_men1_avg_calories = bg_cal(spark, valuemid1, gropman1.count())

    gropwomen1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen1 = gropwomen1.select('id').collect()
    valuewid1 = [row.id for row in rowsuserwomen1]
    gropwomen1avCalories = bg_cal(spark, valuewid1, gropwomen1.count())

    #  Group 2
    gropman2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender']==1))
    rowsuserman2 = gropman2.select('id').collect()
    valuemid2 = [row.id for row in rowsuserman2]
    group_men2_avg_calories = bg_cal(spark, valuemid2, gropman2.count())

    gropwomen2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender']==2))
    rowsuserwomen2 = gropwomen2.select('id').collect()
    valuewid2 = [row.id for row in rowsuserwomen2]
    group_women2_avg_calories = bg_cal(spark, valuewid2, gropwomen2.count())

    #  Group 3
    gropman3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender'] == 1))
    rowsuserman3 = gropman3.select('id').collect()
    valuemid3 = [row.id for row in rowsuserman3]
    group_men3_avg_calories = bg_cal(spark, valuemid3, gropman3.count())

    gropwomen3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen3 = gropwomen3.select('id').collect()
    valuewid3 = [row.id for row in rowsuserwomen3]
    group_women3_avg_calories = bg_cal(spark, valuewid3, gropwomen3.count())

    #  Group 4
    gropman4 = dfusers.filter( ((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender'] == 1))
    rowsuserman4 = gropman4.select('id').collect()
    valuemid4 = [row.id for row in rowsuserman4]
    group_men4_avg_calories = bg_cal(spark, valuemid4, gropman4.count())

    gropwomen4 = dfusers.filter(((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender'] == 2))
    rowsuserwomen4 = gropwomen4.select('id').collect()
    valuewid4 = [row.id for row in rowsuserwomen4]
    group_women4_avg_calories = bg_cal(spark, valuewid4, gropwomen4.count())

    #  Group 5
    gropman5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender'] == 1))
    rowsuserman5 = gropman5.select('id').collect()
    valuemid5 = [row.id for row in rowsuserman5]
    group_men5_avg_calories = bg_cal(spark, valuemid5, gropman5.count())

    gropwomen5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender'] == 2))
    rowsuserwomen5 = gropwomen5.select('id').collect()
    valuewid5 = [row.id for row in rowsuserwomen5]
    group_women5_avg_calories = bg_cal(spark, valuewid5, gropwomen5.count())

    input_schema = StructType(
        [
            StructField("ID", StringType(), True),
            StructField("age_group", StringType(), True),
            StructField("men_average_bg", FloatType(), True),
            StructField("women_average_bg", FloatType(), True),
        ])
    input_data = [
        ("1", "2-5歲", group_men1_avg_calories,gropwomen1avCalories),
        ("2", "6-11歲", group_men2_avg_calories,group_women2_avg_calories),
        ("3", "12-17歲", group_men3_avg_calories,group_women3_avg_calories),
        ("4", "18-64歲", group_men4_avg_calories,group_women4_avg_calories),
        ("5", "65歲以上", group_men5_avg_calories,group_women5_avg_calories),
    ]
    input_df = spark.createDataFrame(data=input_data, schema=input_schema)
    return input_df

def avg_bp (spark):
    dfusers = process_data(spark,config,"users")
    #  Group 1
    gropman1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender_id']==1))
    rowsuserman1 = gropman1.select('id').collect()
    valuemid1 = [row.id for row in rowsuserman1]
    gp1_men_avg_sys_bp = bp_cal(spark, valuemid1, gropman1.count())[0]

    gropman1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender_id']==1))
    rowsuserman1 = gropman1.select('id').collect()
    valuemid1 = [row.id for row in rowsuserman1]
    gp1_men_avg_dia_bp = bp_cal(spark, valuemid1, gropman1.count())[1]

    gropwomen1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender_id'] == 2))
    rowsuserwomen1 = gropwomen1.select('id').collect()
    valuewid1 = [row.id for row in rowsuserwomen1]
    gp1_women_avg_sys_bp = bp_cal(spark, valuewid1, gropwomen1.count())[0]

    gropwomen1 = dfusers.filter(((dfusers['birthday']) < '2020-12-31') & ((dfusers['birthday']) > '2017-01-01') & (dfusers['gender_id'] == 2))
    rowsuserwomen1 = gropwomen1.select('id').collect()
    valuewid1 = [row.id for row in rowsuserwomen1]
    gp1_women_avg_dia_bp = bp_cal(spark, valuewid1, gropwomen1.count())[1]

    # #  Group 2
    gropman2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender_id']==1))
    rowsuserman2 = gropman2.select('id').collect()
    valuemid2 = [row.id for row in rowsuserman2]
    gp2_men_avg_sys_bp = bp_cal(spark, valuemid2, gropman2.count())[0]

    gropman2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender_id']==1))
    rowsuserman2 = gropman2.select('id').collect()
    valuemid2 = [row.id for row in rowsuserman2]
    gp2_men_avg_dia_bp = bp_cal(spark, valuemid2, gropman2.count())[1]

    gropwomen2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender_id']==2))
    rowsuserwomen2 = gropwomen2.select('id').collect()
    valuewid2 = [row.id for row in rowsuserwomen2]
    gp2_women_avg_sys_bp = bp_cal(spark, valuewid2, gropwomen2.count())[0]

    gropwomen2 = dfusers.filter(((dfusers['birthday']) < '2017-12-31') & ((dfusers['birthday']) > '2011-01-01') & (dfusers['gender_id']==2))
    rowsuserwomen2 = gropwomen2.select('id').collect()
    valuewid2 = [row.id for row in rowsuserwomen2]
    gp2_women_avg_dia_bp = bp_cal(spark, valuewid2, gropwomen2.count())[1]


    # #  Group 3
    gropman3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender_id'] == 1))
    rowsuserman3 = gropman3.select('id').collect()
    valuemid3 = [row.id for row in rowsuserman3]
    gp3_men_avg_sys_bp = bp_cal(spark, valuemid3, gropman3.count())[0]

    gropman3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender_id'] == 1))
    rowsuserman3 = gropman3.select('id').collect()
    valuemid3 = [row.id for row in rowsuserman3]
    gp3_men_avg_dia_bp = bp_cal(spark, valuemid3, gropman3.count())[1]

    gropwomen3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender_id'] == 2))
    rowsuserwomen3 = gropwomen3.select('id').collect()
    valuewid3 = [row.id for row in rowsuserwomen3]
    gp3_women_avg_sys_bp = bp_cal(spark, valuewid3, gropwomen3.count())[0]

    gropwomen3 = dfusers.filter(((dfusers['birthday']) < '2011-12-31') & ((dfusers['birthday']) > '2005-01-01') & (dfusers['gender_id'] == 2))
    rowsuserwomen3 = gropwomen3.select('id').collect()
    valuewid3 = [row.id for row in rowsuserwomen3]
    gp3_women_avg_dia_bp = bp_cal(spark, valuewid3, gropwomen3.count())[1]


    # #  Group 4
    gropman4 = dfusers.filter( ((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender_id'] == 1))
    rowsuserman4 = gropman4.select('id').collect()
    valuemid4 = [row.id for row in rowsuserman4]
    gp4_men_avg_sys_bp = bp_cal(spark, valuemid4, gropman4.count())[0]

    gropman4 = dfusers.filter( ((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender_id'] == 1))
    rowsuserman4 = gropman4.select('id').collect()
    valuemid4 = [row.id for row in rowsuserman4]
    gp4_men_avg_dia_bp = bp_cal(spark, valuemid4, gropman4.count())[1]

    gropwomen4 = dfusers.filter(((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender_id'] == 2))
    rowsuserwomen4 = gropwomen4.select('id').collect()
    valuewid4 = [row.id for row in rowsuserwomen4]
    gp4_women_avg_sys_bp = bp_cal(spark, valuewid4, gropwomen4.count())[0]

    gropwomen4 = dfusers.filter(((dfusers['birthday']) < '2005-12-31') & ((dfusers['birthday']) > '1958-01-01') & (dfusers['gender_id'] == 2))
    rowsuserwomen4 = gropwomen4.select('id').collect()
    valuewid4 = [row.id for row in rowsuserwomen4]
    gp4_women_avg_dia_bp = bp_cal(spark, valuewid4, gropwomen4.count())[1]

    # #  Group 5
    gropman5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender_id'] == 1))
    rowsuserman5 = gropman5.select('id').collect()
    valuemid5 = [row.id for row in rowsuserman5]
    gp5_men_avg_sys_bp = bp_cal(spark, valuemid5, gropman5.count())[0]

    gropman5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender_id'] == 1))
    rowsuserman5 = gropman5.select('id').collect()
    valuemid5 = [row.id for row in rowsuserman5]
    gp5_men_avg_dia_bp = bp_cal(spark, valuemid5, gropman5.count())[1]

    gropwomen5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender_id'] == 2))
    rowsuserwomen5 = gropwomen5.select('id').collect()
    valuewid5 = [row.id for row in rowsuserwomen5]
    gp5_women_avg_sys_bp = bp_cal(spark, valuewid5, gropwomen5.count())[0]

    gropwomen5 = dfusers.filter(((dfusers['birthday']) < '1958-12-31')  & (dfusers['gender_id'] == 2))
    rowsuserwomen5 = gropwomen5.select('id').collect()
    valuewid5 = [row.id for row in rowsuserwomen5]
    gp5_women_avg_dia_bp = bp_cal(spark, valuewid5, gropwomen5.count())[1]

    input_schema = StructType(
        [
            StructField("ID", StringType(), True),
            StructField("age_group", StringType(), True),
            StructField("men_average_sys_bp", FloatType(), True),
            StructField("men_average_dia_bp", FloatType(), True),
            StructField("women_average_sys_bp", FloatType(), True),
            StructField("women_average_dia_bp", FloatType(), True),
        ])
    input_data = [
        ("1", "2-5歲", gp1_men_avg_sys_bp, gp1_men_avg_dia_bp, gp1_women_avg_sys_bp, gp1_women_avg_dia_bp),
        ("2", "6-11歲", gp2_men_avg_sys_bp, gp2_men_avg_dia_bp, gp2_women_avg_sys_bp, gp2_women_avg_dia_bp),
        ("3", "12-17歲", gp3_men_avg_sys_bp, gp3_men_avg_dia_bp, gp3_women_avg_sys_bp, gp3_women_avg_dia_bp),
        ("4", "18-65歲", gp4_men_avg_sys_bp, gp4_men_avg_dia_bp, gp4_women_avg_sys_bp, gp4_women_avg_dia_bp),
        ("5", "65歲以上", gp5_men_avg_sys_bp, gp5_men_avg_dia_bp, gp5_women_avg_sys_bp, gp5_women_avg_dia_bp),
    ]
    input_df = spark.createDataFrame(data=input_data, schema=input_schema)
    return input_df

def main():
    spark = prepare_spark(config)
    df = process_data(spark, config, "users")

    df_avg_bg = avg_bg(spark)
    df_avg_bg.show()


    df_avg_bp = avg_bp(spark)
    df_avg_bp.show()

    save_data(df_avg_bp, "avg_bp")

    df_avg_ex = avg_ex_cal(spark)

    df_avg_cal_breakfast = cal_calories(spark, 1).withColumnRenamed("men_average_calories","men_average_calories_br")\
        .withColumnRenamed("women_average_calories","women_average_calories_br")

    df_avg_cal_lunch = cal_calories(spark, 2).withColumnRenamed("men_average_calories","men_average_calories_lunch")\
        .withColumnRenamed("women_average_calories","women_average_calories_lunch")

    df_avg_cal_dinner = cal_calories(spark, 3).withColumnRenamed("men_average_calories","men_average_calories_din")\
        .withColumnRenamed("women_average_calories","women_average_calories_din")

    df_avg_cal_snack = cal_calories(spark, 4).withColumnRenamed("men_average_calories","men_average_calories_snack")\
        .withColumnRenamed("women_average_calories","women_average_calories_snack")

    df_diet_cal_brief = df_avg_cal_breakfast.alias("a").join(df_avg_cal_lunch.alias("b"), df_avg_cal_breakfast['ID'] == df_avg_cal_lunch ['ID'])\
        .join(df_avg_cal_dinner.alias("c"), df_avg_cal_breakfast['ID'] == df_avg_cal_dinner['ID'])\
        .join(df_avg_cal_snack.alias("d"), df_avg_cal_breakfast['ID'] == df_avg_cal_snack['ID'])\
        .join(df_avg_ex.alias("e"), df_avg_cal_breakfast['ID'] == df_avg_ex['ID'])\
        .select("a.ID","a.age_group","a.men_average_calories_br", "a.women_average_calories_br", "b.men_average_calories_lunch", "b.women_average_calories_lunch","c.men_average_calories_din","c.women_average_calories_din", "d.men_average_calories_snack", "d.women_average_calories_snack","e.men_average_ex_cal_burned","e.women_average_ex_cal_burned")\
    
    df_cal_sum = df_diet_cal_brief.withColumn("men_diet_sum", df_diet_cal_brief["men_average_calories_br"] + df_diet_cal_brief["men_average_calories_lunch"] + df_diet_cal_brief["men_average_calories_din"] + df_diet_cal_brief["men_average_calories_snack"])\
        .withColumn("women_diet_sum", df_diet_cal_brief["women_average_calories_br"] + df_diet_cal_brief["women_average_calories_lunch"] + df_diet_cal_brief["women_average_calories_din"] + df_diet_cal_brief["women_average_calories_snack"])\
    
    df_net_cal = df_cal_sum.withColumn("men_net_cal", df_cal_sum["men_diet_sum"] - df_cal_sum["men_average_ex_cal_burned"])\
        .withColumn("women_net_cal", df_cal_sum["women_diet_sum"] - df_cal_sum["women_average_ex_cal_burned"])


    save_data(df_net_cal, "df_net_cal")
    df_net_cal.show()

    # nutrition_stats:

    df_avg_nutrition_protein = avg_nutrition_cal(spark, "protein").withColumnRenamed("men_average_nutrition_intake","men_average_protein_intake")\
        .withColumnRenamed("women_average_nutrition_intake","women_average_protein_intake")
    
    df_avg_nutrition_protein.show()

    df_avg_nutrition_carbo = avg_nutrition_cal(spark, "carbohydrates").withColumnRenamed("men_average_nutrition_intake","men_average_carbo_intake")\
        .withColumnRenamed("women_average_nutrition_intake","women_average_carbo_intake")

    df_avg_nutrition_carbo.show()

    df_avg_nutrition_fat = avg_nutrition_cal(spark, "fat").withColumnRenamed("men_average_nutrition_intake","men_average_fat_intake")\
        .withColumnRenamed("women_average_nutrition_intake","women_average_fat_intake")

    df_avg_nutrition_fat.show()

    df_avg_nutrition_fiber = avg_nutrition_cal(spark, "fiber").withColumnRenamed("men_average_nutrition_intake","men_average_fiber_intake")\
        .withColumnRenamed("women_average_nutrition_intake","women_average_fiber_intake")  
    
    df_avg_nutrition_fiber.show()

    df_avg_nutrition_sugars = avg_nutrition_cal(spark, "sugars").withColumnRenamed("men_average_nutrition_intake","men_average_sugars_intake")\
        .withColumnRenamed("women_average_nutrition_intake","women_average_sugars_intake")

    df_avg_nutrition_sugars.show()

    df_avg_nutrition_sodium = avg_nutrition_cal(spark, "sodium").withColumnRenamed("men_average_nutrition_intake","men_average_sodium_intake")\
        .withColumnRenamed("women_average_nutrition_intake","women_average_sodium_intake")

    df_avg_nutrition_sodium.show()

    df_avg_nutrition_summary = df_avg_nutrition_protein.alias("p").join(df_avg_nutrition_carbo.alias("c"), df_avg_nutrition_protein['ID'] == df_avg_nutrition_carbo['ID'])\
        .join(df_avg_nutrition_fat.alias("fa"), df_avg_nutrition_protein['ID'] == df_avg_nutrition_fat['ID'])\
        .join(df_avg_nutrition_fiber.alias("fi"), df_avg_nutrition_protein['ID'] == df_avg_nutrition_fiber['ID'])\
        .join(df_avg_nutrition_sugars.alias("su"), df_avg_nutrition_protein['ID'] == df_avg_nutrition_sugars['ID'])\
        .join(df_avg_nutrition_sodium.alias("so"), df_avg_nutrition_protein['ID'] == df_avg_nutrition_sodium['ID'])\
        .select("p.ID","p.age_group","p.men_average_protein_intake", "p.women_average_protein_intake", "c.men_average_carbo_intake", "c.women_average_carbo_intake", "fa.men_average_fat_intake", "fa.men_average_fat_intake", "fi.men_average_fiber_intake","fi.women_average_fiber_intake","su.men_average_sugars_intake", "su.women_average_sugars_intake", "so.men_average_sodium_intake", "so.women_average_sodium_intake")\
        .show()

    
    count1 = df.filter(((df['birthday']) < '2020-12-31') & ((df['birthday']) > '2017-01-01')).count()
    count2 = df.filter(((df['birthday']) < '2017-12-31') & ((df['birthday']) > '2011-01-01')).count()
    count3 = df.filter(((df['birthday']) < '2011-12-31') & ((df['birthday']) > '2005-01-01')).count()
    count4 = df.filter(((df['birthday']) < '2005-12-31') & ((df['birthday']) > '1958-01-01')).count()
    count5 = df.filter(((df['birthday']) < '1958-12-31')).count()
    input_schema = StructType(
        [
            StructField("ID", StringType(), True),
            StructField("age_group", StringType(), True),
            StructField("counts", IntegerType(), True),
        ])
    input_data = [
        ("1","2-5歲", count1),
        ("2","6-11歲", count2),
        ("3","12-17歲", count3),
        ("4","18-64歲", count4),
        ("5","65歲以上", count5),
    ]
    age_group_df = spark.createDataFrame(data=input_data, schema=input_schema)
    
    save_data(age_group_df, "age_group")

    mancount1,mancount2,mancount3,mancount4,mancount5 = mancount(df)
    input_schema = StructType(
        [
            StructField("ID", StringType(), True),
            StructField("Age group", StringType(), True),
            StructField("Men", StringType(), True),
            StructField("Women", StringType(), True),
        ])
    input_data = [
        ("1", "2-5歲", mancount1, count1-mancount1),
        ("2", "6-11歲", mancount2, count2-mancount2),
        ("3", "12-17歲", mancount3, count3-mancount3),
        ("4", "18-64歲", mancount4, count4-mancount4),
        ("5", "65歲以上", mancount5, count5-mancount5),
    ]
    input_df = spark.createDataFrame(data=input_data, schema=input_schema)
    input_df.show()

    df2 = process_data(spark, config, "users")
    df_profession_stats = mancount_pf_el(df2, 'profession')
    df_gender_stats = mancount_pf_el(df2, 'gender')
    df_education_stats = mancount_pf_el(df2, 'education')
    df_chronic_condition_stats = mancount_pf_el(df2, 'chronic_condition')

if __name__ == "__main__":
    main()
