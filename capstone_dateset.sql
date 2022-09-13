CREATE TABLE profession_types(
    id SERIAL PRIMARY KEY,
    pf_type TEXT
);

INSERT INTO profession_types (pf_type) VALUES ('學生'); --id : 1  student
INSERT INTO profession_types (pf_type) VALUES ('廣告及設計'); --id : 2  Advertising and marketing
INSERT INTO profession_types (pf_type) VALUES ('資訊及通訊科技'); --id : 3  Computer and technology
INSERT INTO profession_types (pf_type) VALUES ('建造'); --id : 4  Construction
INSERT INTO profession_types (pf_type) VALUES ('教育'); --id : 5  Education
INSERT INTO profession_types (pf_type) VALUES ('藝術及演藝'); --id : 6  Fashion and Art
INSERT INTO profession_types (pf_type) VALUES ('金融及銀行'); --id : 7  Finance and Banking
INSERT INTO profession_types (pf_type) VALUES ('工程'); --id : 8  Engineering
INSERT INTO profession_types (pf_type) VALUES ('醫療及護理服務'); --id : 9  Health care
INSERT INTO profession_types (pf_type) VALUES ('工業及製造'); --id : 10  Manufacturing
INSERT INTO profession_types (pf_type) VALUES ('酒店、飲食及旅遊'); --id : 11 Hotel, Catering and Tourism
INSERT INTO profession_types (pf_type) VALUES ('物流及運輸'); --id : 12  Transportation
INSERT INTO profession_types (pf_type) VALUES ('零售及進出口貿易'); --id : 13  Wholesale and retail
INSERT INTO profession_types (pf_type) VALUES ('退休'); --id : 14  retired
INSERT INTO profession_types (pf_type) VALUES ('其他'); --id : 15  others


CREATE TABLE chronic_condition(
    id SERIAL PRIMARY KEY,
    disease TEXT
);

INSERT INTO chronic_condition (disease) VALUES ('無'); --id : 1  none
INSERT INTO chronic_condition (disease) VALUES ('糖尿病'); --id : 2  diabetes
INSERT INTO chronic_condition (disease) VALUES ('關節炎'); --id : 3  arthritis
INSERT INTO chronic_condition (disease) VALUES ('心血管疾病'); --id : 4  heart disease
INSERT INTO chronic_condition (disease) VALUES ('癌症'); --id : 5  cancer
INSERT INTO chronic_condition (disease) VALUES ('慢性呼吸道疾病'); --id : 6  respiratory disease
INSERT INTO chronic_condition (disease) VALUES ('認知障礙'); --id : 7  Alzheimer disease
INSERT INTO chronic_condition (disease) VALUES ('腎功能疾病'); --id : 8  kidney disease
INSERT INTO chronic_condition (disease) VALUES ('其他'); --id : 9  others

CREATE TABLE gender(
    id SERIAL PRIMARY KEY,
    gender_type TEXT
);

INSERT INTO gender (gender_type) VALUES ('男'); --id : 1  male
INSERT INTO gender (gender_type) VALUES ('女'); --id : 2  female
INSERT INTO gender (gender_type) VALUES ('其他'); --id : 3  other


CREATE TABLE education(
    id SERIAL PRIMARY KEY,
    education_level TEXT
);

INSERT INTO education (education_level) VALUES ('小學或以下'); --id : 1  
INSERT INTO education (education_level) VALUES ('中學'); --id : 2  
INSERT INTO education (education_level) VALUES ('專上教育'); --id : 3  
INSERT INTO education (education_level) VALUES ('學士學位'); --id : 4  
INSERT INTO education (education_level) VALUES ('碩士學位'); --id : 5  
INSERT INTO education (education_level) VALUES ('博士學位'); --id : 6  


CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL, 
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    height INTEGER NOT NULL,
    weight INTEGER NOT NULL,
    gender INTEGER NOT NULL,
    FOREIGN KEY(gender) REFERENCES gender(id),
    phone VARCHAR(8) NOT NULL,
    address VARCHAR(255) NOT NULL,
    profession INTEGER,
    FOREIGN KEY(profession) REFERENCES profession_types(id),
    hkid VARCHAR(8) NOT NULL,
    chronic_condition INTEGER,
    FOREIGN KEY(chronic_condition) REFERENCES chronic_condition(id),
    education INTEGER NOT NULL,
    FOREIGN KEY(education) REFERENCES education(id),
    is_deleted BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

----users: 0-5 yrs-----
INSERT INTO users (username, first_name, last_name, email, password, birthday, height, weight, gender, phone, address, profession, hkid, chronic_condition, education, is_deleted, created_at, updated_at) VALUES ('peterzhang', 'Peter', 'Zhang', 'peterzhang@gmail.com', '34325f3', '2021-09-08', 50, 10, 1, '23455467', 'fsdfsfsdf', 1, 'W2340512', 6, 1, FALSE, NOW(), NOW()); 
INSERT INTO users (username, first_name, last_name, email, password, birthday, height, weight, gender, phone, address, profession, hkid, chronic_condition, education, is_deleted, created_at, updated_at) VALUES ('williamwang', 'William', 'Wang', 'williamwang@gmail.com', 'ff43tsf', '2018-01-03', 45, 20, 1, '21349087', 'sf45fdgdlo,sads2', 1, 'Z1234567', 1, 1, FALSE, NOW(), NOW());

INSERT INTO users (username, first_name, last_name, email, password, birthday, height, weight, gender, phone, address, profession, hkid, chronic_condition, education, is_deleted, created_at, updated_at) VALUES ('gigiliu', 'Gigi', 'Liu', 'gigiliu@gmail.com', 'sasd32dsad', '2019-03-05', 43, 9, 2, '34561789', 'sf45fdgdlo,sd,sads2', 1, 'A1234567', 1, 1, FALSE, NOW(), NOW()); 

----users: 6-11 yrs-----
INSERT INTO users (username, first_name, last_name, email, password, birthday, height, weight, gender, phone, address, profession, hkid, chronic_condition, education, is_deleted, created_at, updated_at) VALUES ('benxu', 'Ben', 'Xu', 'benxu@gmail.com', '234t56fvg', '2016-04-05', 85, 20, 1, '45671555', 'csdf43fd,dfe43,sads2', 1, 'B1255567', 4, 1, FALSE, NOW(), NOW()); 
INSERT INTO users (username, first_name, last_name, email, password, birthday, height, weight, gender, phone, address, profession, hkid, chronic_condition, education, is_deleted, created_at, updated_at) VALUES ('fayezhao', 'Faye', 'Zhao', 'fayezhao@gmail.com', '23423444', '2017-09-12', 80, 35, 1, '33330901', '124,sd,sads2', 1, 'F1234217', 9, 1, FALSE, NOW(), NOW()); 
INSERT INTO users (username, first_name, last_name, email, password, birthday, height, weight, gender, phone, address, profession, hkid, chronic_condition, education, is_deleted, created_at, updated_at) VALUES ('mickywu', 'Micky', 'Wu', 'mickywu@gmail.com', '123dcvghfghghj', '2017-03-05', 75, 27, 2, '23334501', 's11111,sd,sads2', 1, 'C1111167', 1, 1, FALSE, NOW(), NOW()); 




CREATE TABLE users_weight(
    id SERIAL PRIMARY KEY,
    weight INTEGER,
    date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO users_weight (weight, date, created_at, updated_at, user_id) VALUES (20, '2022-09-06', NOW(), NOW(), 1); 


CREATE TABLE users_blood_glucose(
    id SERIAL PRIMARY KEY,
    bg_measurement INTEGER,
    date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 
INSERT INTO users_blood_glucose (bg_measurement, date, created_at, updated_at, user_id) VALUES (50, '2022-09-06', NOW(), NOW(), 1); 



CREATE TABLE users_blood_pressure(
    id SERIAL PRIMARY KEY,
    sys_bp INTEGER,
    dia_bp INTEGER,
    date DATE,
    created_at TIMESTAMP,
    uploaded_at TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO users_blood_pressure (sys_bp, dia_bp, created_at, uploaded_at, user_id) VALUES (100, 70, NOW(), 1); 


CREATE TABLE diets_types(
    id SERIAL PRIMARY KEY,
    d_type TEXT
);

INSERT INTO diets_types (d_type) VALUES ('早餐'); --id : 1  breakfast
INSERT INTO diets_types (d_type) VALUES ('午餐'); --id : 2  lunch
INSERT INTO diets_types (d_type) VALUES ('晚餐'); --id : 3  dinner
INSERT INTO diets_types (d_type) VALUES ('小食'); --id : 4  snack


CREATE TABLE food_groups(
    id SERIAL PRIMARY KEY,
    food_group TEXT
);

INSERT INTO food_groups (food_group) VALUES ('穀類'); --id : 1  穀類及其製品
INSERT INTO food_groups (food_group) VALUES ('豆類'); --id : 2  豆類及其製品
INSERT INTO food_groups (food_group) VALUES ('蔬菜類'); --id : 3  蔬菜類及其製品
INSERT INTO food_groups (food_group) VALUES ('水果類'); --id : 4  水果類及其製品
INSERT INTO food_groups (food_group) VALUES ('堅果與種子'); --id : 5  堅果與種子及其製品
INSERT INTO food_groups (food_group) VALUES ('畜肉類'); --id : 6  畜肉類及其製品
INSERT INTO food_groups (food_group) VALUES ('禽肉類'); --id : 7  禽肉類及其製品
INSERT INTO food_groups (food_group) VALUES ('蛋類'); --id : 8  蛋類及其製品
INSERT INTO food_groups (food_group) VALUES ('奶類及其製品'); --id : 9  奶類及其製品
INSERT INTO food_groups (food_group) VALUES ('冰凍甜點'); --id : 10  冰凍甜點
INSERT INTO food_groups (food_group) VALUES ('魚類'); --id : 11  魚類及其製品
INSERT INTO food_groups (food_group) VALUES ('不含酒精飲料'); --id : 12  不含酒精飲料
INSERT INTO food_groups (food_group) VALUES ('糖及糖類製品'); --id : 13 糖及糖類製品
INSERT INTO food_groups (food_group) VALUES ('湯類'); --id : 14 湯類
INSERT INTO food_groups (food_group) VALUES ('小食'); --id : 15 小食
INSERT INTO food_groups (food_group) VALUES ('即食食物'); --id : 16 即食食物


CREATE TABLE food(
    id SERIAL PRIMARY KEY,
    food_name VARCHAR(255),
    group_id INTEGER,
    FOREIGN KEY(group_id) REFERENCES food_groups(id),
    food_calories NUMERIC(8,4),
    carbohydrates NUMERIC(8,4),
    sugars NUMERIC(8,4),
    fat NUMERIC(8,4),
    protein NUMERIC(8,4),
    fiber NUMERIC(8,4),
    sodium NUMERIC(8,4)
);

COPY food(food_name, group_id, food_calories, carbohydrates, sugars, fat, protein, fiber, sodium) FROM '/Users/austin/Downloads/food1.csv' DELIMITER ',' CSV HEADER;

INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('A bowl of rice', 1, 200, 30, 5, 5, 10, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('A bowl of noodle', 1, 200, 30, 5, 5, 10, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('Apple', 2, 50, 5, 10, 1, 1, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('Orange', 2, 50, 5, 10, 1, 1, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('Tomato', 3, 50, 5, 0, 1, 1, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('Cabbage', 3, 50, 5, 0, 1, 1, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('Beef', 4, 100, 20, 0, 10, 10, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('Chicken', 4, 100, 20, 0, 10, 10, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('Milk', 5, 50, 10, 5, 5, 5, 5, 50);
INSERT INTO food (name, group_id, calories, carbohydrates, sugars, fat, protein, fiber, sodium) VALUES ('yogurt', 5, 50, 10, 5, 5, 5, 5, 50);


CREATE TABLE users_diets(
    id SERIAL PRIMARY KEY,
    diet_type INTEGER,
    FOREIGN KEY(diet_type) REFERENCES diets_types(id),
    food INTEGER,
    FOREIGN KEY(food) REFERENCES food(id),
    food_amount NUMERIC(5,2),
    date DATE,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    created_at TIMESTAMP,
    uploaded_at TIMESTAMP
);

-- Example of a person(id=1) 's breakfast:
INSERT INTO users_diets (diet_type, food, food_amount, date, user_id, created_at, uploaded_at) VALUES (1, 2, 1, '2022-09-03', 1);
INSERT INTO users_diets (diet_type, food, food_amount, date, user_id, created_at, uploaded_at) VALUES (1, 2, 1, '2022-09-03', 1);


CREATE TABLE exercises_types(
    id SERIAL PRIMARY KEY,
    ex_type VARCHAR(255),
    ex_calories INTEGER
);

-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('walk/run, moderate', 290); --id : 1  walk/run, moderate
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('walk/run, vigorous', 363); --id : 2  walk/run, vigorous
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Football', 508); --id : 3  Football
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Basketball', 581); --id : 4  Basketball
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Swimming, vigorous', 726); --id : 5  Swimming, vigorous
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Swimming, moderate', 290); --id : 6  Swimming, moderate
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Climbing hills', 545); --id : 7  Climbing hills
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Martial arts, kick boxing', 726); --id : 8  Martial arts, kick boxing
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Weight lifting', 217); --id : 9  Weight lifting
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Cycling, moderate', 581); --id : 10  Cycling, moderate
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Cycling, vigorous', 726); --id : 11  Cycling, vigorous
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Cycling, leisure', 290); --id : 12  Cycling, leisure
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Whitewater rafting, kayaking, canoeing', 363); --id : 13  Whitewater rafting, kayaking, canoeing
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Table tennis', 290); --id : 14  Table tennis
-- INSERT INTO exercises (exercise_name, exercise_cal) VALUES ('Tennis', 508); --id : 15  Tennis

INSERT INTO exercises (ex_type, ex_calories) VALUES ('跑步/行走, 中等程度', 290); --id : 1  walk/run, moderate
INSERT INTO exercises (ex_type, ex_calories) VALUES ('跑步/行走, 劇烈程度', 363); --id : 2  walk/run, vigorous
INSERT INTO exercises (ex_type, ex_calories) VALUES ('足球', 508); --id : 3  Football
INSERT INTO exercises (ex_type, ex_calories) VALUES ('籃球', 581); --id : 4  Basketball
INSERT INTO exercises (ex_type, ex_calories) VALUES ('游泳, 中等程度', 726); --id : 5  Swimming, vigorous
INSERT INTO exercises (ex_type, ex_calories) VALUES ('游泳, 劇烈程度', 290); --id : 6  Swimming, moderate
INSERT INTO exercises (ex_type, ex_calories) VALUES ('擧石', 545); --id : 7  Climbing hills
INSERT INTO exercises (ex_type, ex_calories) VALUES ('自由搏擊, 踢拳', 726); --id : 8  Martial arts, kick boxing
INSERT INTO exercises (ex_type, ex_calories) VALUES ('舉重', 217); --id : 9  Weight lifting
INSERT INTO exercises (ex_type, ex_calories) VALUES ('踏單車, 中等程度', 581); --id : 10  Cycling, moderate
INSERT INTO exercises (ex_type, ex_calories) VALUES ('踏單車, 劇烈程度', 726); --id : 11  Cycling, vigorous
INSERT INTO exercises (ex_type, ex_calories) VALUES ('踏單車, 休閑程度', 290); --id : 12  Cycling, leisure
INSERT INTO exercises (ex_type, ex_calories) VALUES ('泛舟, 划艇, 划獨木舟', 363); --id : 13  Whitewater rafting, kayaking, canoeing
INSERT INTO exercises (ex_type, ex_calories) VALUES ('乒乓波', 290); --id : 14  Table tennis
INSERT INTO exercises (ex_type, ex_calories) VALUES ('網球', 508); --id : 15  Tennis


CREATE TABLE users_exercises(
    id SERIAL PRIMARY KEY,
    date DATE,
    exercise_id INTEGER,
    FOREIGN KEY(exercise_id) REFERENCES exercises(id),
    exercise_duration DECIMAL(2,1),
    user_id INTEGER,
    created_at TIMESTAMP,
    uploaded_at TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    recorded_at TIMESTAMP
);

INSERT INTO users_exercise (exercise_id, exercise_duration, user_id, recorded_at) VALUES (1, 1, 1, '2022-09-03');
