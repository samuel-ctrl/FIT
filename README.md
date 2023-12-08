# WATER MONITOR

**Timeline for recommended water intake by age, height, weight, and body problems**

**Age** | **Liters per day**
------- | --------
0-6 months | 0.75-0.85
6-12 months | 0.85-1.2
1-3 years | 1.2-1.6
4-8 years | 1.6-2.1
9-13 years | 2.1-2.6
14-18 years | 2.6-3.2
Adults (men) | 3.0-3.7
Adults (women) | 2.2-2.7
Pregnant women | 2.7-3.0
Breastfeeding women | 3.1-3.8

**Height** | **Liters per day**
-------- | --------
Below 150 cm | 2.5-3.0
150-160 cm | 3.0-3.5
160-170 cm | 3.5-4.0
170-180 cm | 4.0-4.5
Above 180 cm | 4.5-5.0

**Weight** | **Liters per day**
-------- | --------
Below 50 kg | 1.7-2.1
50-60 kg | 2.1-2.5
60-70 kg | 2.5-2.9
70-80 kg | 2.9-3.3
80-90 kg | 3.3-3.7
Above 90 kg | 3.7-4.1

**Body problems** | **Recommendations**
-------- | --------
Diabetes | Drink more water than usual to prevent dehydration.
Kidney disease | Limit your fluid intake depending on your doctor's recommendation.
Heart disease | Limit your fluid intake depending on your doctor's recommendation.
Diarrhea | Drink plenty of fluids to replace lost fluids and electrolytes.
Vomiting | Drink small amounts of fluids frequently to avoid dehydration.

**General tips for staying hydrated**

* Drink water throughout the day, even if you're not thirsty.
* Drink more water when you're sweating, such as when you're exercising or in hot weather.
* Avoid sugary drinks, such as soda and juice, as they can dehydrate you.
* Eat fruits and vegetables, which are high in water content.

If you have any questions or concerns about how much water you should drink, talk to your doctor.

# CALCULATION BASED OF WEIGHT, HEIGHT, AGE, HEALTH CONDITION

```
Minimum average: (age_min + height_min + weight_min) / 3 = water liters per day

Maximum average: (age_max + height_max + weight_max) / 3 = water liters per day

Note: According to the health condition water consumption will change.
some health condition need more than average as well as some condition need less than average.
```

## WATER CONTENT IN HUMAN BODY

### **60% WATER**
- Up to 60% of the human adult body is water. According to Mitchell and others (1945), the brain and heart are composed of 73% water, and the lungs are about 83% water. The skin contains 64% water, muscles and kidneys are 79%, and even the bones are watery: 31%.

- The average percentage of water in your body may vary depending on sex, age, and weight. That said, more than half of your body weight is composed of water starting at birth.

- Fatty tissue contains less water than lean tissue# WITAR

## Recommended Feature needed for our app :-

- **Personalized water intake recommendations:** The app could take into account the user's age, height, weight, activity level, and health conditions to calculate a personalized water intake goal.

- **Water tracking by beverage:** The app could allow users to track their water intake by beverage type, such as water, coffee, tea, and juice. This could help users to identify which beverages are contributing to their hydration and which ones are dehydrating them.

- **Water intake reminders:** The app could send users reminder notifications throughout the day to drink water. This could be especially helpful for people who are busy and forget to drink enough water.

- **Water quality tracking:** The app could integrate with water quality sensors to track the quality of the user's drinking water. This could help users to identify and avoid drinking water that is contaminated.

- **Water usage tracking:** The app could track the user's water usage at home and send them alerts if they are using too much water. This could help users to conserve water and save money on their water bill.

- **Integration with other health and fitness apps:** The app could integrate with other health and fitness apps, such as step trackers and calorie counters. This would allow users to see how their water intake is related to other aspects of their health and fitness.

- **Gamification**: Incorporate elements of gaming, such as rewards, badges, and challenges, to make achieving hydration goals fun and engaging.

- **Water Intake Recommendations**: The application will provide users with recommended daily water intake based on their age, height, and weight. This data will be presented in a clear and easy-to-understand table format.

- **Hydration Tips**: In addition to personalized water intake recommendations, the application will also provide general tips for staying hydrated.

- **Water Intake Calculation**: The application will calculate the minimum and maximum average water intake based on the user's age, height, and weight. This calculation will also take into account any health conditions the user may have.

- **Water Content in the Human Body**: The application will also provide information about the water content in different parts of the human body. This information can help users understand the importance of staying hydrated.

- **Health Conditions**: The application will also take into account the user's health conditions, such as diabetes, kidney disease, heart disease, diarrhea, and vomiting. Recommendations for water intake will be adjusted accordingly.

## HIGH-LEVEL DATABASE SCHEMA DESIGN:

**Entities**

* Users: Stores user information, including name, age, height, weight, activity level, health conditions, and hydration goals.
* Beverages: Stores beverage information, including type, water content, and caffeine content.
* Water Intake: Stores water intake records, including date, time, beverage type, amount consumed, and associated notes.
<!-- * Water Quality: Stores water quality data, including date, time, location, temperature, pH, conductivity, and contaminant levels. -->
* Reminders: Stores reminder information, including reminder type (water intake, water quality check), frequency, and notification settings.
* Badges: Stores badge information, including badge name, description, and unlocking criteria.
* Challenges: Stores challenge information, including challenge name, description, duration, goals, and rewards.

**Relationships**

* Users have many Water Intake records.
* Users have many Water Quality records.
* Users have many Water Usage records.
* Users have many Reminders.
* Users earn Badges.
* Users participate in Challenges.
* Beverages have many Water Intake records.
* Water Intake records are associated with Users.
* Water Intake records are associated with Beverages.
* Water Quality records are associated with Users.
* Water Usage records are associated with Users.
* Reminders are associated with Users.
* Badges are awarded to Users.
* Challenges are assigned to Users.