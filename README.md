# C21-Capstone-Project-Dataset-Gp1
The dataset of capstone proj. gp1


profession_types (pf_type) VALUES ('學生'); --id : 1  student
profession_types (pf_type) VALUES ('廣告及設計'); --id : 2  Advertising and marketing
profession_types (pf_type) VALUES ('資訊及通訊科技'); --id : 3  Computer and technology
profession_types (pf_type) VALUES ('建造'); --id : 4  Construction
profession_types (pf_type) VALUES ('教育'); --id : 5  Education
profession_types (pf_type) VALUES ('藝術及演藝'); --id : 6  Fashion and Art
profession_types (pf_type) VALUES ('金融及銀行'); --id : 7  Finance and Banking
profession_types (pf_type) VALUES ('工程'); --id : 8  Engineering
profession_types (pf_type) VALUES ('醫療及護理服務'); --id : 9  Health care
profession_types (pf_type) VALUES ('工業及製造'); --id : 10  Manufacturing
profession_types (pf_type) VALUES ('酒店、飲食及旅遊'); --id : 11 Hotel, Catering and Tourism
profession_types (pf_type) VALUES ('物流及運輸'); --id : 12  Transportation
profession_types (pf_type) VALUES ('零售及進出口貿易'); --id : 13  Wholesale and retail
profession_types (pf_type) VALUES ('退休'); --id : 14  retired
profession_types (pf_type) VALUES ('其他'); --id : 15  others

INSERT INTO chronic_condition (disease) VALUES ('無'); --id : 1  none
INSERT INTO chronic_condition (disease) VALUES ('糖尿病'); --id : 2  diabetes
INSERT INTO chronic_condition (disease) VALUES ('關節炎'); --id : 3  arthritis
INSERT INTO chronic_condition (disease) VALUES ('心血管疾病'); --id : 4  heart disease
INSERT INTO chronic_condition (disease) VALUES ('癌症'); --id : 5  cancer
INSERT INTO chronic_condition (disease) VALUES ('慢性呼吸道疾病'); --id : 6  respiratory disease
INSERT INTO chronic_condition (disease) VALUES ('認知障礙'); --id : 7  Alzheimer disease
INSERT INTO chronic_condition (disease) VALUES ('腎功能疾病'); --id : 8  kidney disease
INSERT INTO chronic_condition (disease) VALUES ('其他'); --id : 9  others

INSERT INTO gender (gender_type) VALUES ('男'); --id : 1  male
INSERT INTO gender (gender_type) VALUES ('女'); --id : 2  female
INSERT INTO gender (gender_type) VALUES ('其他'); --id : 3  other


INSERT INTO education (education_level) VALUES ('小學或以下'); --id : 1  
INSERT INTO education (education_level) VALUES ('中學'); --id : 2  
INSERT INTO education (education_level) VALUES ('專上教育'); --id : 3  
INSERT INTO education (education_level) VALUES ('學士學位'); --id : 4  
INSERT INTO education (education_level) VALUES ('碩士學位'); --id : 5  
INSERT INTO education (education_level) VALUES ('博士學位'); --id : 6  


INSERT INTO users_auth (auth_type) VALUES ('用戶'); --id : 1  user
INSERT INTO users_auth (auth_type) VALUES ('營養師'); --id : 2 dietitian

INSERT INTO diets_types (d_type) VALUES ('早餐'); --id : 1  breakfast
INSERT INTO diets_types (d_type) VALUES ('午餐'); --id : 2  lunch
INSERT INTO diets_types (d_type) VALUES ('晚餐'); --id : 3  dinner
INSERT INTO diets_types (d_type) VALUES ('小食'); --id : 4  snack


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
