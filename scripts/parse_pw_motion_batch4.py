import json

# Questions 61 to 90 data
b4_data = [
    {
        "num": 61,
        "statement": "Two paper screens A and B are separated by distance 100 m. A bullet penetrates A and B, at points P and Q respectively, where Q is 10 cm below P. If bullet is travelling horizontally at the time of hitting A, the velocity of bullet at A is nearly",
        "options": [
            {"index": 1, "optionText": "100 m/s", "isCorrect": False, "studentPercentage": "31.54%"},
            {"index": 2, "optionText": "200 m/s", "isCorrect": False, "studentPercentage": "33.67%"},
            {"index": 3, "optionText": "600 m/s", "isCorrect": False, "studentPercentage": "14.21%"},
            {"index": 4, "optionText": "700 m/s", "isCorrect": True, "studentPercentage": "20.58%"}
        ],
        "correctOption": "D",
        "accuracy": "20.69%",
        "accuracyPct": 20.69,
        "difficulty": "Hard",
        "solutionText": "Vertical drop h = 10 cm = 0.1 m. Time of flight t = sqrt(2h/g) = sqrt(2 * 0.1 / 9.8) = sqrt(0.2/9.8) ≈ 0.1428 s. Horizontal distance d = 100 m. Horizontal velocity v = d / t = 100 / 0.1428 ≈ 700 m/s."
    },
    {
        "num": 62,
        "statement": "The graph given shows the POSITION of two cars, A and B, as a function of time. The cars move along the x-axis on parallel but separate tracks, so that they can pass each others position without colliding. At which instant in time is car-A overtaking the car-B?",
        "options": [
            {"index": 1, "optionText": "t1", "isCorrect": True, "studentPercentage": "55.11%"},
            {"index": 2, "optionText": "t2", "isCorrect": False, "studentPercentage": "22.38%"},
            {"index": 3, "optionText": "t3", "isCorrect": False, "studentPercentage": "18.51%"},
            {"index": 4, "optionText": "t4", "isCorrect": False, "studentPercentage": "5.11%"}
        ],
        "correctOption": "A",
        "accuracy": "54.28%",
        "accuracyPct": 54.28,
        "difficulty": "Medium",
        "solutionText": "At time t1, position of car A exceeds car B with a steeper positive slope (higher velocity), indicating car A overtakes car B at t1."
    },
    {
        "num": 63,
        "statement": "If the velocity of a particle is given by v = (180 - 16x)^(1/2) m/s, then its acceleration will be",
        "options": [
            {"index": 1, "optionText": "0", "isCorrect": False, "studentPercentage": "12.64%"},
            {"index": 2, "optionText": "8 m/s^2", "isCorrect": False, "studentPercentage": "21.11%"},
            {"index": 3, "optionText": "-8 m/s^2", "isCorrect": True, "studentPercentage": "55.58%"},
            {"index": 4, "optionText": "4 m/s^2", "isCorrect": False, "studentPercentage": "10.72%"}
        ],
        "correctOption": "C",
        "accuracy": "55.34%",
        "accuracyPct": 55.34,
        "difficulty": "Medium",
        "solutionText": "v^2 = 180 - 16x. Differentiating w.r.t x: 2v (dv/dx) = -16 => a = v (dv/dx) = -8 m/s^2."
    },
    {
        "num": 64,
        "statement": "A 210-meter long train is moving due north at a speed of 25 m/s. A small bird is flying due South a little above the train with a speed of 5 m/s. The time taken by the bird to cross the train is",
        "options": [
            {"index": 1, "optionText": "6 s", "isCorrect": False, "studentPercentage": "12.30%"},
            {"index": 2, "optionText": "7 s", "isCorrect": True, "studentPercentage": "60.68%"},
            {"index": 3, "optionText": "9 s", "isCorrect": False, "studentPercentage": "15.41%"},
            {"index": 4, "optionText": "10 s", "isCorrect": False, "studentPercentage": "11.62%"}
        ],
        "correctOption": "B",
        "accuracy": "60.68%",
        "accuracyPct": 60.68,
        "difficulty": "Easy",
        "solutionText": "Relative speed = v_train + v_bird = 25 + 5 = 30 m/s. Length of train = 210 m. Time taken = 210 / 30 = 7 s."
    },
    {
        "num": 65,
        "statement": "In a one dimensional motion, position 'x' and time 't' are related as t = sqrt(x) + 3, where x is in metre and t is in seconds. Speed of the particle after 6 seconds is",
        "options": [
            {"index": 1, "optionText": "4 m/s", "isCorrect": False, "studentPercentage": "11.84%"},
            {"index": 2, "optionText": "2 m/s", "isCorrect": False, "studentPercentage": "21.75%"},
            {"index": 3, "optionText": "6 m/s", "isCorrect": True, "studentPercentage": "59.72%"},
            {"index": 4, "optionText": "8 m/s", "isCorrect": False, "studentPercentage": "6.69%"}
        ],
        "correctOption": "C",
        "accuracy": "59.72%",
        "accuracyPct": 59.72,
        "difficulty": "Easy",
        "solutionText": "sqrt(x) = t - 3 => x = (t - 3)^2. Velocity v = dx/dt = 2(t - 3). At t = 6 s: v = 2(6 - 3) = 6 m/s."
    },
    {
        "num": 66,
        "statement": "Study the following v-t graphs in column I carefully and match appropriately with the statements given in column-II. Assume that motion takes place from time 0 to T.",
        "options": [
            {"index": 1, "optionText": "(A)-Q,S; (B)-P,S; (C)-R,T; (D)-P,T", "isCorrect": True, "studentPercentage": "100.00%"},
            {"index": 2, "optionText": "(A)-P,S; (B)-R,T; (C)-P,T; (D)-Q,S", "isCorrect": False, "studentPercentage": "0.00%"},
            {"index": 3, "optionText": "(A)-R,T; (B)-P,T; (C)-Q,S; (D)-P,S", "isCorrect": False, "studentPercentage": "0.00%"},
            {"index": 4, "optionText": "(A)-P,T; (B)-Q,S; (C)-P,S; (D)-R,T", "isCorrect": False, "studentPercentage": "0.00%"}
        ],
        "correctOption": "A",
        "accuracy": "100.0%",
        "accuracyPct": 100.0,
        "difficulty": "Medium",
        "solutionText": "Matching v-t curves with sign of acceleration (slope) and sign of velocity yields code (1): (A)-Q,S; (B)-P,S; (C)-R,T; (D)-P,T."
    },
    {
        "num": 67,
        "statement": "The magnitude of average velocity is equal to the average speed when a particle moves:",
        "options": [
            {"index": 1, "optionText": "On a curved path", "isCorrect": False, "studentPercentage": "6.96%"},
            {"index": 2, "optionText": "In the same direction", "isCorrect": True, "studentPercentage": "67.23%"},
            {"index": 3, "optionText": "With constant acceleration", "isCorrect": False, "studentPercentage": "22.49%"},
            {"index": 4, "optionText": "With constant retardation", "isCorrect": False, "studentPercentage": "3.44%"}
        ],
        "correctOption": "B",
        "accuracy": "67.35%",
        "accuracyPct": 67.35,
        "difficulty": "Easy",
        "solutionText": "|Average velocity| = |Displacement| / time, and Average speed = Distance / time. |Displacement| = Distance only when motion is in a straight line along the same direction without reversing."
    },
    {
        "num": 68,
        "statement": "A car starts with constant acceleration a=2 m/s^2 at t=0. Two coins are released from the car at t=3 s and t=4 s. Each coin takes 1 s to fall on ground. Then the distance between the two coins will be (Assume coin sticks to the ground)",
        "options": [
            {"index": 1, "optionText": "6 m", "isCorrect": False, "studentPercentage": "17.37%"},
            {"index": 2, "optionText": "7 m", "isCorrect": False, "studentPercentage": "40.04%"},
            {"index": 3, "optionText": "8 m", "isCorrect": False, "studentPercentage": "22.49%"},
            {"index": 4, "optionText": "9 m", "isCorrect": True, "studentPercentage": "20.20%"}
        ],
        "correctOption": "D",
        "accuracy": "20.29%",
        "accuracyPct": 20.29,
        "difficulty": "Hard",
        "solutionText": "Position of 1st coin released at t=3: x1 = 1/2 a t^2 = 1/2(2)(9) = 9 m. Horizontal velocity v1 = a*t = 2(3) = 6 m/s. Horizontal travel while falling in 1 s: 6 m. Total landing position: 9 + 6 = 15 m. Position of 2nd coin released at t=4: x2 = 1/2(2)(16) = 16 m. Horizontal velocity v2 = 2(4) = 8 m/s. Horizontal travel while falling in 1 s: 8 m. Total landing position: 16 + 8 = 24 m. Distance between coins = 24 - 15 = 9 m."
    },
    {
        "num": 69,
        "statement": "Statement-I : A particle moves in a straight line with constant acceleration. The average velocity of this particle cannot be zero in any time interval. Statement-II : For a particle moving in straight line with constant acceleration, the average velocity in a time interval is (u+v)/2, where u and v are initial and final velocity of the particle.",
        "options": [
            {"index": 1, "optionText": "Statement-1 is true, Statement-2 is true ; Statement-2 is correct explanation", "isCorrect": False, "studentPercentage": "33.33%"},
            {"index": 2, "optionText": "Statement-1 is true, Statement-2 is true ; Statement-2 is NOT a correct explanation", "isCorrect": False, "studentPercentage": "0.00%"},
            {"index": 3, "optionText": "Statement-1 is true, Statement-2 is false", "isCorrect": False, "studentPercentage": "33.33%"},
            {"index": 4, "optionText": "Statement-1 is false, Statement-2 is true", "isCorrect": True, "studentPercentage": "33.33%"}
        ],
        "correctOption": "D",
        "accuracy": "33.33%",
        "accuracyPct": 33.33,
        "difficulty": "Medium",
        "solutionText": "A particle thrown vertically upward returns to the thrower at t = 2u/g, having zero displacement and therefore zero average velocity. Hence Statement-I is false. Statement-II is mathematically true for uniform acceleration: v_avg = (u + v) / 2."
    },
    {
        "num": 70,
        "statement": "Object is moving with constant speed then velocity of object",
        "options": [
            {"index": 1, "optionText": "may be variable", "isCorrect": True, "studentPercentage": "47.54%"},
            {"index": 2, "optionText": "must be constant", "isCorrect": False, "studentPercentage": "32.81%"},
            {"index": 3, "optionText": "must be variable", "isCorrect": False, "studentPercentage": "7.41%"},
            {"index": 4, "optionText": "may be zero", "isCorrect": False, "studentPercentage": "12.23%"}
        ],
        "correctOption": "A",
        "accuracy": "47.54%",
        "accuracyPct": 47.54,
        "difficulty": "Easy",
        "solutionText": "Velocity is a vector quantity having magnitude (speed) and direction. Even if speed is constant, direction can change (e.g., in uniform circular motion), so velocity may be variable."
    },
    {
        "num": 71,
        "statement": "Consider the following statements and select the incorrect statements. I. Instantaneous velocity magnitude = instantaneous speed. II. Average velocity magnitude = average speed. III. Speed never zero but average speed zero. IV. Speed zero but average speed not zero.",
        "options": [
            {"index": 1, "optionText": "II, III and IV", "isCorrect": False, "studentPercentage": "39.00%"},
            {"index": 2, "optionText": "I and II", "isCorrect": False, "studentPercentage": "19.23%"},
            {"index": 3, "optionText": "II and III", "isCorrect": True, "studentPercentage": "25.29%"},
            {"index": 4, "optionText": "IV only", "isCorrect": False, "studentPercentage": "16.47%"}
        ],
        "correctOption": "C",
        "accuracy": "25.29%",
        "accuracyPct": 25.29,
        "difficulty": "Medium",
        "solutionText": "Statements II and III are incorrect: |v_avg| <= speed_avg, and speed cannot be non-zero while average speed is zero."
    },
    {
        "num": 72,
        "statement": "Speed of two identical cars are u and 4u at a specific instant. The ratio of the respective distances in which the two cars are stopped from that instant is:",
        "options": [
            {"index": 1, "optionText": "1 : 1", "isCorrect": False, "studentPercentage": "8.41%"},
            {"index": 2, "optionText": "1 : 4", "isCorrect": False, "studentPercentage": "26.22%"},
            {"index": 3, "optionText": "1 : 8", "isCorrect": False, "studentPercentage": "12.52%"},
            {"index": 4, "optionText": "1 : 16", "isCorrect": True, "studentPercentage": "53.42%"}
        ],
        "correctOption": "D",
        "accuracy": "53.23%",
        "accuracyPct": 53.23,
        "difficulty": "Easy",
        "solutionText": "Stopping distance s = u^2 / (2a). For identical cars with same braking deceleration a, s ∝ u^2. Therefore, s1 / s2 = u^2 / (4u)^2 = 1 / 16."
    },
    {
        "num": 73,
        "statement": "A man standing on the edge of the terrace of a high rise building throws a stone vertically up with a speed of 20 m/s. Two seconds later an identical stone is thrown vertically downwards with the same speed of 20 m/s. Which of the following statement is incorrect?",
        "options": [
            {"index": 1, "optionText": "relative velocity between the two stones remain constant", "isCorrect": False, "studentPercentage": "33.98%"},
            {"index": 2, "optionText": "both will have the same kinetic energy when they hit ground", "isCorrect": False, "studentPercentage": "34.62%"},
            {"index": 3, "optionText": "the time interval between their hitting the ground is 4 seconds", "isCorrect": True, "studentPercentage": "27.71%"},
            {"index": 4, "optionText": "if collisions perfectly elastic both will rise to same height", "isCorrect": False, "studentPercentage": "24.22%"}
        ],
        "correctOption": "C",
        "accuracy": "27.71%",
        "accuracyPct": 27.71,
        "difficulty": "Hard",
        "solutionText": "The first stone returns to terrace level after t = 2u/g = 2(20)/10 = 4 s with speed 20 m/s downward. The second stone was thrown downward after 2 s. Hence the time interval between them passing the terrace downward is 4 - 2 = 2 s, not 4 s. Statement 3 is incorrect."
    },
    {
        "num": 74,
        "statement": "The v-t plot of a moving object is shown in the figure. The average velocity of the object during the first 10 seconds is",
        "options": [
            {"index": 1, "optionText": "0", "isCorrect": True, "studentPercentage": "67.39%"},
            {"index": 2, "optionText": "2.5 ms^-1", "isCorrect": False, "studentPercentage": "15.94%"},
            {"index": 3, "optionText": "5 ms^-1", "isCorrect": False, "studentPercentage": "11.59%"},
            {"index": 4, "optionText": "2 ms^-1", "isCorrect": False, "studentPercentage": "5.07%"}
        ],
        "correctOption": "A",
        "accuracy": "67.39%",
        "accuracyPct": 67.39,
        "difficulty": "Easy",
        "solutionText": "Total displacement = Area under v-t graph = Area above time axis - Area below time axis = 0. Therefore, average velocity = 0 / 10 = 0."
    },
    {
        "num": 75,
        "statement": "The position of a particle moving on a straight line path is given by : x = 12 + 18t + 9t^2 metre, Its acceleration at t = 5 s is:",
        "options": [
            {"index": 1, "optionText": "9 ms^-2", "isCorrect": False, "studentPercentage": "8.73%"},
            {"index": 2, "optionText": "12 ms^-2", "isCorrect": False, "studentPercentage": "11.26%"},
            {"index": 3, "optionText": "18 ms^-2", "isCorrect": True, "studentPercentage": "71.20%"},
            {"index": 4, "optionText": "45 ms^-2", "isCorrect": False, "studentPercentage": "8.73%"}
        ],
        "correctOption": "C",
        "accuracy": "71.90%",
        "accuracyPct": 71.9,
        "difficulty": "Easy",
        "solutionText": "v = dx/dt = 18 + 18t. a = dv/dt = 18 ms^-2 (constant for all t, including t = 5 s)."
    },
    {
        "num": 76,
        "statement": "Even when we are sleeping, air moves into and out of our lungs and blood flow in arteries and veins. With reference to the above statement, which of the following statement(s) is/are correct?",
        "options": [
            {"index": 1, "optionText": "Only I", "isCorrect": False, "studentPercentage": "33.33%"},
            {"index": 2, "optionText": "Only II", "isCorrect": False, "studentPercentage": "0.00%"},
            {"index": 3, "optionText": "Both II and III", "isCorrect": True, "studentPercentage": "66.67%"},
            {"index": 4, "optionText": "Both I and II", "isCorrect": False, "studentPercentage": "0.00%"}
        ],
        "correctOption": "C",
        "accuracy": "66.67%",
        "accuracyPct": 66.67,
        "difficulty": "Easy",
        "solutionText": "In everyday biological processes, motion is continuous and reference frame dependent. Statements II and III are physically correct."
    },
    {
        "num": 77,
        "statement": "For the one-dimensional motion, described by x = t - sin(t) :",
        "options": [
            {"index": 1, "optionText": "x(t) > 0 for all t > 0", "isCorrect": True, "studentPercentage": "37.50%"},
            {"index": 2, "optionText": "v(t) > 0 for all t > 0", "isCorrect": False, "studentPercentage": "32.60%"},
            {"index": 3, "optionText": "a(t) > 0 for all t > 0", "isCorrect": False, "studentPercentage": "17.01%"},
            {"index": 4, "optionText": "v(t) lies between 0 and 3", "isCorrect": False, "studentPercentage": "11.98%"}
        ],
        "correctOption": "A",
        "accuracy": "37.37%",
        "accuracyPct": 37.37,
        "difficulty": "Medium",
        "solutionText": "For t > 0, t > sin(t) strictly, so x(t) = t - sin(t) > 0 for all t > 0. Velocity v(t) = 1 - cos(t) = 0 at t = 2nπ, so v(t) is not strictly > 0 everywhere."
    },
    {
        "num": 78,
        "statement": "A body thrown vertically upward with velocity 10 m/s then how many height travelled by body.",
        "options": [
            {"index": 1, "optionText": "5 m", "isCorrect": True, "studentPercentage": "58.68%"},
            {"index": 2, "optionText": "10 m", "isCorrect": False, "studentPercentage": "25.09%"},
            {"index": 3, "optionText": "15 m", "isCorrect": False, "studentPercentage": "9.91%"},
            {"index": 4, "optionText": "20 m", "isCorrect": False, "studentPercentage": "6.49%"}
        ],
        "correctOption": "A",
        "accuracy": "58.42%",
        "accuracyPct": 58.42,
        "difficulty": "Easy",
        "solutionText": "H_max = u^2 / (2g) = 10^2 / (2 * 10) = 100 / 20 = 5 m."
    },
    {
        "num": 79,
        "statement": "A stone thrown upward with a speed u from the top of a tower reaches the ground with a velocity 4u. The height of the tower is",
        "options": [
            {"index": 1, "optionText": "15u^2 / 2g", "isCorrect": True, "studentPercentage": "46.71%"},
            {"index": 2, "optionText": "7u^2 / 2g", "isCorrect": False, "studentPercentage": "13.83%"},
            {"index": 3, "optionText": "16u^2 / g", "isCorrect": False, "studentPercentage": "30.96%"},
            {"index": 4, "optionText": "Zero", "isCorrect": False, "studentPercentage": "8.37%"}
        ],
        "correctOption": "A",
        "accuracy": "46.71%",
        "accuracyPct": 46.71,
        "difficulty": "Medium",
        "solutionText": "v^2 = u^2 + 2gh => (4u)^2 = u^2 + 2gh => 16u^2 - u^2 = 2gh => h = 15u^2 / (2g)."
    },
    {
        "num": 80,
        "statement": "The acceleration a in ms^-2 of a particle is given by a = 3t^2 + 2t + 2, where t is the time. If the particle starts out with a velocity u = 2 ms^-1 at t = 0, find velocity at end of 2 s.",
        "options": [
            {"index": 1, "optionText": "16 m/s", "isCorrect": False, "studentPercentage": "29.88%"},
            {"index": 2, "optionText": "18 m/s", "isCorrect": True, "studentPercentage": "50.24%"},
            {"index": 3, "optionText": "36 m/s", "isCorrect": False, "studentPercentage": "16.27%"},
            {"index": 4, "optionText": "9 m/s", "isCorrect": False, "studentPercentage": "3.86%"}
        ],
        "correctOption": "B",
        "accuracy": "50.12%",
        "accuracyPct": 50.12,
        "difficulty": "Easy",
        "solutionText": "v(t) = u + ∫ a dt = 2 + ∫_0^2 (3t^2 + 2t + 2) dt = 2 + [t^3 + t^2 + 2t]_0^2 = 2 + (8 + 4 + 4) = 18 m/s."
    },
    {
        "num": 81,
        "statement": "A passenger train of length 60 m travels at a speed of 80 km/h. Another freight train of length 120 m travels at a speed of 30 km/h. The ratio of times taken by passenger train to completely cross the freight train when (i) moving in same direction and (ii) opposite direction is",
        "options": [
            {"index": 1, "optionText": "3/2", "isCorrect": False, "studentPercentage": "11.00%"},
            {"index": 2, "optionText": "25/11", "isCorrect": False, "studentPercentage": "21.51%"},
            {"index": 3, "optionText": "11/5", "isCorrect": True, "studentPercentage": "62.76%"},
            {"index": 4, "optionText": "5/2", "isCorrect": False, "studentPercentage": "4.79%"}
        ],
        "correctOption": "C",
        "accuracy": "62.90%",
        "accuracyPct": 62.9,
        "difficulty": "Medium",
        "solutionText": "Relative speed in same direction = 80 - 30 = 50 km/h. In opposite direction = 80 + 30 = 110 km/h. Distance is the same (L1 + L2 = 180 m). Ratio of times t_same / t_opp = v_opp / v_same = 110 / 50 = 11/5."
    },
    {
        "num": 82,
        "statement": "A bus starts from rest moving with an acceleration of 2 m/s^2. A cyclist, 96 m behind the bus starts simultaneously towards the bus at 20 m/s. After what time will he be able to overtake the bus :",
        "options": [
            {"index": 1, "optionText": "8 s", "isCorrect": True, "studentPercentage": "40.00%"},
            {"index": 2, "optionText": "10 s", "isCorrect": False, "studentPercentage": "30.13%"},
            {"index": 3, "optionText": "12 s", "isCorrect": False, "studentPercentage": "24.81%"},
            {"index": 4, "optionText": "1 s", "isCorrect": False, "studentPercentage": "4.98%"}
        ],
        "correctOption": "A",
        "accuracy": "40.00%",
        "accuracyPct": 40.0,
        "difficulty": "Medium",
        "solutionText": "x_bus = 1/2 (2) t^2 = t^2. x_cyclist = 20t - 96. Equating: t^2 = 20t - 96 => t^2 - 20t + 96 = 0 => (t - 8)(t - 12) = 0. Earliest overtake time is t = 8 s."
    },
    {
        "num": 83,
        "statement": "Two trains A and B, 100 m and 60 m long, are moving in opposite directions on parallel tracks. The velocity of the shorter train is 3 times that of the larger one. If the trains take 4 s to cross each other, the velocities of the trains are:",
        "options": [
            {"index": 1, "optionText": "vA = 10 ms^-1, vB = 30 ms^-1", "isCorrect": True, "studentPercentage": "48.72%"},
            {"index": 2, "optionText": "vA = 2.5 ms^-1, vB = 7.5 ms^-1", "isCorrect": False, "studentPercentage": "23.41%"},
            {"index": 3, "optionText": "vA = 20 ms^-1, vB = 60 ms^-1", "isCorrect": False, "studentPercentage": "21.57%"},
            {"index": 4, "optionText": "vA = 5 ms^-1, vB = 15 ms^-1", "isCorrect": False, "studentPercentage": "6.75%"}
        ],
        "correctOption": "A",
        "accuracy": "48.33%",
        "accuracyPct": 48.33,
        "difficulty": "Easy",
        "solutionText": "Total distance = 100 + 60 = 160 m. Relative speed = 160 / 4 = 40 m/s. Let v_larger = v, v_shorter = 3v. v + 3v = 40 => 4v = 40 => v = 10 m/s, 3v = 30 m/s."
    },
    {
        "num": 84,
        "statement": "A car travels the first half of a distance between two places at a speed of 30 km/hr and the second half of the distance at 50 km/hr. The average speed of the car for the whole journey is",
        "options": [
            {"index": 1, "optionText": "42.5 km/hr", "isCorrect": False, "studentPercentage": "50.00%"},
            {"index": 2, "optionText": "40.0 km/hr", "isCorrect": False, "studentPercentage": "0.00%"},
            {"index": 3, "optionText": "37.5 km/hr", "isCorrect": True, "studentPercentage": "50.00%"},
            {"index": 4, "optionText": "35.0 km/hr", "isCorrect": False, "studentPercentage": "0.00%"}
        ],
        "correctOption": "C",
        "accuracy": "50.00%",
        "accuracyPct": 50.0,
        "difficulty": "Easy",
        "solutionText": "v_avg = 2 * v1 * v2 / (v1 + v2) = 2 * 30 * 50 / (30 + 50) = 3000 / 80 = 37.5 km/hr."
    },
    {
        "num": 85,
        "statement": "Two trains are each 50 m long moving parallel towards each other at speeds 10 m/s and 15 m/s respectively, at what time will they pass each other?",
        "options": [
            {"index": 1, "optionText": "8 s", "isCorrect": False, "studentPercentage": "16.43%"},
            {"index": 2, "optionText": "4 s", "isCorrect": True, "studentPercentage": "45.06%"},
            {"index": 3, "optionText": "2 s", "isCorrect": False, "studentPercentage": "31.71%"},
            {"index": 4, "optionText": "6 s", "isCorrect": False, "studentPercentage": "6.93%"}
        ],
        "correctOption": "B",
        "accuracy": "45.06%",
        "accuracyPct": 45.06,
        "difficulty": "Easy",
        "solutionText": "Total distance = 50 + 50 = 100 m. Relative speed = 10 + 15 = 25 m/s. Time = 100 / 25 = 4 s."
    },
    {
        "num": 86,
        "statement": "The graph between displacement x and time t for a particle moving in a straight line is shown in figure. During interval OA, AB, BC, CD, the acceleration of particle is:",
        "options": [
            {"index": 1, "optionText": "+ 0 + +", "isCorrect": False, "studentPercentage": "34.07%"},
            {"index": 2, "optionText": "- 0 + 0", "isCorrect": True, "studentPercentage": "45.22%"},
            {"index": 3, "optionText": "+ 0 - +", "isCorrect": False, "studentPercentage": "16.42%"},
            {"index": 4, "optionText": "- 0 - +", "isCorrect": False, "studentPercentage": "4.29%"}
        ],
        "correctOption": "B",
        "accuracy": "45.22%",
        "accuracyPct": 45.22,
        "difficulty": "Medium",
        "solutionText": "OA is concave downward (a < 0). AB is a straight line (a = 0). BC is concave upward (a > 0). CD is horizontal/linear (a = 0). Signs: - 0 + 0."
    },
    {
        "num": 87,
        "statement": "A ball is thrown vertically upwards with a velocity of 40 ms^-1 from the top of a multistorey building of 25 m high. How high will the ball rise?",
        "options": [
            {"index": 1, "optionText": "20 m", "isCorrect": False, "studentPercentage": "12.01%"},
            {"index": 2, "optionText": "80 m", "isCorrect": True, "studentPercentage": "66.91%"},
            {"index": 3, "optionText": "40 m", "isCorrect": False, "studentPercentage": "16.52%"},
            {"index": 4, "optionText": "10 m", "isCorrect": False, "studentPercentage": "4.71%"}
        ],
        "correctOption": "B",
        "accuracy": "66.81%",
        "accuracyPct": 66.81,
        "difficulty": "Easy",
        "solutionText": "Height risen above the building h = u^2 / (2g) = 40^2 / (2 * 10) = 1600 / 20 = 80 m."
    },
    {
        "num": 88,
        "statement": "The slope of velocity position graph of a particle moving along a straight line is 15 units where velocity is also 15 units. The acceleration of particle at that position is :-",
        "options": [
            {"index": 1, "optionText": "1 unit", "isCorrect": False, "studentPercentage": "30.50%"},
            {"index": 2, "optionText": "75 unit", "isCorrect": False, "studentPercentage": "15.99%"},
            {"index": 3, "optionText": "225 unit", "isCorrect": True, "studentPercentage": "44.28%"},
            {"index": 4, "optionText": "30 unit", "isCorrect": False, "studentPercentage": "8.86%"}
        ],
        "correctOption": "C",
        "accuracy": "44.03%",
        "accuracyPct": 44.03,
        "difficulty": "Easy",
        "solutionText": "Acceleration a = v (dv/dx) = 15 * 15 = 225 units."
    },
    {
        "num": 89,
        "statement": "Two trains each 50 m long, are travelling in opposite directions with respective velocities 10 m/s and 15 m/s. The time of crossing is",
        "options": [
            {"index": 1, "optionText": "2 s", "isCorrect": False, "studentPercentage": "22.22%"},
            {"index": 2, "optionText": "4 s", "isCorrect": True, "studentPercentage": "50.79%"},
            {"index": 3, "optionText": "2/3 s", "isCorrect": False, "studentPercentage": "21.36%"},
            {"index": 4, "optionText": "4/3 s", "isCorrect": False, "studentPercentage": "6.20%"}
        ],
        "correctOption": "B",
        "accuracy": "50.22%",
        "accuracyPct": 50.22,
        "difficulty": "Easy",
        "solutionText": "Total distance = 50 + 50 = 100 m. Relative speed = 10 + 15 = 25 m/s. Time of crossing = 100 / 25 = 4 s."
    },
    {
        "num": 90,
        "statement": "A stone falls freely under gravity. It covers distances h1, h2 and h3 in the first 5 seconds, the next 5 seconds and the next 5 seconds respectively. The relation between h1, h2 and h3 is",
        "options": [
            {"index": 1, "optionText": "h1 = h2/3 = h3/5", "isCorrect": True, "studentPercentage": "68.49%"},
            {"index": 2, "optionText": "h2 = 3h1 and h3 = 3h2", "isCorrect": False, "studentPercentage": "14.43%"},
            {"index": 3, "optionText": "h1 = h2 = h3", "isCorrect": False, "studentPercentage": "11.16%"},
            {"index": 4, "optionText": "h1 = 2h2 = 3h3", "isCorrect": False, "studentPercentage": "5.99%"}
        ],
        "correctOption": "A",
        "accuracy": "68.54%",
        "accuracyPct": 68.54,
        "difficulty": "Easy",
        "solutionText": "By Galileo's law of odd numbers for equal consecutive time intervals from rest, h1 : h2 : h3 = 1 : 3 : 5 => h1 = h2/3 = h3/5."
    }
]

processed = []
for b in b4_data:
    num = b["num"]
    q_data = {
        "id": f"PW_PHY_MOTION1D_{num:03d}",
        "subject": "Physics",
        "chapter": "Motion in a Straight Line",
        "topic": "Kinematics 1D",
        "questionNumber": num,
        "questionType": "Single Choice",
        "statement": b["statement"],
        "options": b["options"],
        "correctOption": b["correctOption"],
        "correctAnswer": b["correctOption"],
        "accuracy": b["accuracy"],
        "accuracyPct": b["accuracyPct"],
        "difficulty": b["difficulty"],
        "solutionText": b["solutionText"],
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice",
        "cohort": "Class 11 IIT JEE"
    }
    processed.append(q_data)

print(f"Prepared {len(processed)} questions from Batch 4.")

# Append to pw_extracted_master.json
with open("pw_extracted_master.json", "r", encoding="utf-8") as f:
    master = json.load(f)

existing_ids = set(x.get("id") for x in master)
added_count = 0
for p in processed:
    if p["id"] not in existing_ids:
        master.append(p)
        added_count += 1
    else:
        for i, ex in enumerate(master):
            if ex.get("id") == p["id"]:
                master[i] = p
                break

with open("pw_extracted_master.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Successfully appended {added_count} new questions to pw_extracted_master.json!")
print(f"New total in pw_extracted_master.json: {len(master)}")
