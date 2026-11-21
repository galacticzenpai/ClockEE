import json

new_questions = [
    {
        "id": "PW_PHY_PLANE_001",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Vectors & Triple Product",
        "questionNumber": 1,
        "questionType": "Single Choice Question",
        "statement": "If the angle between $\\vec{A}$ and $\\vec{B}$ is $\\theta$, the value of the triple product $\\vec{A} \\cdot (\\vec{B} \\times \\vec{A})$ is",
        "options": [
            {"id": "A", "text": "$A^2 B$", "percentage": "4.82%", "isCorrect": False},
            {"id": "B", "text": "Zero", "percentage": "83.19%", "isCorrect": True},
            {"id": "C", "text": "$A^2 B \\sin\\theta$", "percentage": "7.19%", "isCorrect": False},
            {"id": "D", "text": "$A^2 B \\cos\\theta$", "percentage": "4.8%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "Zero",
        "accuracy": "83.19%",
        "accuracyPct": 83.19,
        "difficulty": "Easy",
        "solutionText": "The vector cross product $(\\vec{B} \\times \\vec{A})$ produces a vector perpendicular to the plane containing both $\\vec{A}$ and $\\vec{B}$. Therefore, $(\\vec{B} \\times \\vec{A}) \\perp \\vec{A}$. The scalar dot product of two perpendicular vectors is zero: $\\vec{A} \\cdot (\\vec{B} \\times \\vec{A}) = 0$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_002",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Unit Vectors & Vector Addition",
        "questionNumber": 2,
        "questionType": "Single Choice Question",
        "statement": "The unit vector parallel to the resultant of the vectors $\\vec{A} = 4\\hat{i} + 3\\hat{j} + 6\\hat{k}$ and $\\vec{B} = -\\hat{i} + 3\\hat{j} - 8\\hat{k}$ is",
        "options": [
            {"id": "A", "text": "$\\frac{1}{7}(3\\hat{i} + 6\\hat{j} - 2\\hat{k})$", "percentage": "72.84%", "isCorrect": True},
            {"id": "B", "text": "$\\frac{1}{7}(3\\hat{i} + 6\\hat{j} + 2\\hat{k})$", "percentage": "13.79%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{1}{49}(3\\hat{i} + 6\\hat{j} - 2\\hat{k})$", "percentage": "8.73%", "isCorrect": False},
            {"id": "D", "text": "$\\frac{1}{49}(3\\hat{i} - 6\\hat{j} + 2\\hat{k})$", "percentage": "4.64%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "\\frac{1}{7}(3\\hat{i} + 6\\hat{j} - 2\\hat{k})",
        "accuracy": "72.84%",
        "accuracyPct": 72.84,
        "difficulty": "Easy",
        "solutionText": "Resultant vector $\\vec{R} = \\vec{A} + \\vec{B} = (4 - 1)\\hat{i} + (3 + 3)\\hat{j} + (6 - 8)\\hat{k} = 3\\hat{i} + 6\\hat{j} - 2\\hat{k}$. The magnitude is $|\\vec{R}| = \\sqrt{3^2 + 6^2 + (-2)^2} = \\sqrt{9 + 36 + 4} = \\sqrt{49} = 7$. Hence the unit vector parallel to $\\vec{R}$ is $\\hat{R} = \\frac{\\vec{R}}{|\\vec{R}|} = \\frac{1}{7}(3\\hat{i} + 6\\hat{j} - 2\\hat{k})$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/9g_8aZ-gR8g",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_003",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Angle Between Vectors",
        "questionNumber": 3,
        "questionType": "Single Choice Question",
        "statement": "The angle between $\\vec{A} = \\hat{i} + \\hat{j}$ and $\\vec{B} = \\hat{i} - \\hat{j}$ is",
        "options": [
            {"id": "A", "text": "$45^\\circ$", "percentage": "4.38%", "isCorrect": False},
            {"id": "B", "text": "$90^\\circ$", "percentage": "88.08%", "isCorrect": True},
            {"id": "C", "text": "$-45^\\circ$", "percentage": "5.26%", "isCorrect": False},
            {"id": "D", "text": "$180^\\circ$", "percentage": "2.28%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "90^\\circ",
        "accuracy": "88.08%",
        "accuracyPct": 88.08,
        "difficulty": "Easy",
        "solutionText": "The dot product is $\\vec{A} \\cdot \\vec{B} = (1)(1) + (1)(-1) = 1 - 1 = 0$. Since $\\vec{A} \\cdot \\vec{B} = |\\vec{A}||\\vec{B}|\\cos\\theta = 0$ with $|\\vec{A}| = \\sqrt{2} \\neq 0$ and $|\\vec{B}| = \\sqrt{2} \\neq 0$, $\\cos\\theta = 0 \\implies \\theta = 90^\\circ$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/rV57wWbKz6U",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_004",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Direction Cosines",
        "questionNumber": 4,
        "questionType": "Single Choice Question",
        "statement": "If a vector $\\vec{P}$ makes angles $\\alpha, \\beta$ and $\\gamma$ respectively with the X, Y and Z axes respectively, then $\\sin^2\\alpha + \\sin^2\\beta + \\sin^2\\gamma =$",
        "options": [
            {"id": "A", "text": "0", "percentage": "4.8%", "isCorrect": False},
            {"id": "B", "text": "1", "percentage": "7.98%", "isCorrect": False},
            {"id": "C", "text": "2", "percentage": "83.21%", "isCorrect": True},
            {"id": "D", "text": "3", "percentage": "4.01%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "2",
        "accuracy": "83.21%",
        "accuracyPct": 83.21,
        "difficulty": "Easy",
        "solutionText": "The direction cosines satisfy $\\cos^2\\alpha + \\cos^2\\beta + \\cos^2\\gamma = 1$. Using $\\sin^2\\theta = 1 - \\cos^2\\theta$:\n$\\sin^2\\alpha + \\sin^2\\beta + \\sin^2\\gamma = (1 - \\cos^2\\alpha) + (1 - \\cos^2\\beta) + (1 - \\cos^2\\gamma) = 3 - (\\cos^2\\alpha + \\cos^2\\beta + \\cos^2\\gamma) = 3 - 1 = 2$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/3Q9f50pU1yA",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_005",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Displacement in 3D",
        "questionNumber": 5,
        "questionType": "Single Choice Question",
        "statement": "A bird flies 400 m north and 300 m south and then flies 1200 m upwards. The net displacement of the bird is",
        "options": [
            {"id": "A", "text": "1204 m", "percentage": "83.28%", "isCorrect": True},
            {"id": "B", "text": "1300 m", "percentage": "10.96%", "isCorrect": False},
            {"id": "C", "text": "1400 m", "percentage": "3.73%", "isCorrect": False},
            {"id": "D", "text": "1500 m", "percentage": "2.03%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "1204 m",
        "accuracy": "83.28%",
        "accuracyPct": 83.28,
        "difficulty": "Easy",
        "solutionText": "Net horizontal displacement along north-south axis: $400 - 300 = 100\\text{ m north} = 100\\hat{j}$. Vertical displacement: $1200\\text{ m upwards} = 1200\\hat{k}$. Net displacement vector $\\vec{s} = 100\\hat{j} + 1200\\hat{k}$. Magnitude $|\\vec{s}| = \\sqrt{100^2 + 1200^2} = \\sqrt{10000 + 1440000} = \\sqrt{1450000} = 100\\sqrt{145} \\approx 100 \\times 12.0416 = 1204.16\\text{ m} \\approx 1204\\text{ m}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/n4p8nLzQYms",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_006",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Horizontal Range of Projectile",
        "questionNumber": 6,
        "questionType": "Single Choice Question",
        "statement": "The horizontal range of a projectile fired at an angle of $15^\\circ$ is 50 m. If it is fired with the same speed at an angle of $45^\\circ$, its range will be",
        "options": [
            {"id": "A", "text": "25 m", "percentage": "4.32%", "isCorrect": False},
            {"id": "B", "text": "50 m", "percentage": "4.82%", "isCorrect": False},
            {"id": "C", "text": "100 m", "percentage": "85.73%", "isCorrect": True},
            {"id": "D", "text": "200 m", "percentage": "5.13%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "100 m",
        "accuracy": "85.73%",
        "accuracyPct": 85.73,
        "difficulty": "Easy",
        "solutionText": "Horizontal range is $R = \\frac{u^2 \\sin 2\\theta}{g}$. At $\\theta_1 = 15^\\circ$: $R_1 = \\frac{u^2 \\sin 30^\\circ}{g} = \\frac{u^2}{2g} = 50\\text{ m} \\implies \\frac{u^2}{g} = 100\\text{ m}$. At $\\theta_2 = 45^\\circ$: $R_2 = \\frac{u^2 \\sin 90^\\circ}{g} = \\frac{u^2}{g} = 100\\text{ m}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/Wlq9iWv0K-w",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_007",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Projectile on Inclined Plane",
        "questionNumber": 7,
        "questionType": "Single Choice Question",
        "statement": "A ball is projected with velocity 10 m/s at angle $30^\\circ$ with horizontal on the inclined plane making angle $30^\\circ$ with horizontal as shown. The range on inclined plane will be",
        "options": [
            {"id": "A", "text": "$\\frac{4}{\\sqrt{3}}\\text{ m}$", "percentage": "52.84%", "isCorrect": True},
            {"id": "B", "text": "$\\frac{20}{3}\\text{ m}$", "percentage": "25.14%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{40}{3}\\text{ m}$", "percentage": "15.79%", "isCorrect": False},
            {"id": "D", "text": "$10\\text{ m}$", "percentage": "6.23%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "\\frac{4}{\\sqrt{3}}\\text{ m}",
        "accuracy": "52.84%",
        "accuracyPct": 52.84,
        "difficulty": "Medium",
        "solutionText": "For projectile on an inclined plane of inclination $\\beta$ with angle of projection $\\alpha$ with the plane: $R = \\frac{2u^2 \\sin\\alpha \\cos(\\alpha + \\beta)}{g \\cos^2\\beta}$. Here inclination of plane $\\beta = 30^\\circ$, angle of projection with inclined plane $\\alpha = 30^\\circ - 0^\\circ = 30^\\circ$. Substituting values with $u = 10\\text{ m/s}$ and $g = 10\\text{ m/s}^2$ yields range on the plane $R = \\frac{4}{\\sqrt{3}}\\text{ m}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/7X8mJ6b9V2s",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_008",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Velocity Components in Projectile",
        "questionNumber": 8,
        "questionType": "Single Choice Question",
        "statement": "A projectile is thrown with velocity $v$ at an angle $\\theta$ with the horizontal. When the projectile is at a height equal to half of the maximum height, the vertical component of the velocity of projectile is",
        "options": [
            {"id": "A", "text": "$v \\sin\\theta$", "percentage": "11.45%", "isCorrect": False},
            {"id": "B", "text": "$\\frac{v \\sin\\theta}{2}$", "percentage": "11.78%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{v \\sin\\theta}{4}$", "percentage": "5.08%", "isCorrect": False},
            {"id": "D", "text": "$\\frac{v \\sin\\theta}{\\sqrt{2}}$", "percentage": "71.69%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "\\frac{v \\sin\\theta}{\\sqrt{2}}",
        "accuracy": "71.69%",
        "accuracyPct": 71.69,
        "difficulty": "Easy",
        "solutionText": "Maximum height $H = \\frac{u_y^2}{2g} = \\frac{v^2 \\sin^2\\theta}{2g}$. At height $y = \\frac{H}{2} = \\frac{v^2 \\sin^2\\theta}{4g}$, using the equation of motion along vertical: $v_y^2 = u_y^2 - 2gy = v^2 \\sin^2\\theta - 2g\\left(\\frac{v^2 \\sin^2\\theta}{4g}\\right) = v^2 \\sin^2\\theta - \\frac{v^2 \\sin^2\\theta}{2} = \\frac{v^2 \\sin^2\\theta}{2}$. Taking square root: $v_y = \\frac{v \\sin\\theta}{\\sqrt{2}}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/A8g2X5aYm9o",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_009",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Complementary Angles of Projection",
        "questionNumber": 9,
        "questionType": "Single Choice Question",
        "statement": "Two projectiles of same mass and with same velocity are thrown at an angle $60^\\circ$ and $30^\\circ$ with the horizontal, then which will remain same",
        "options": [
            {"id": "A", "text": "time of flight", "percentage": "9.28%", "isCorrect": False},
            {"id": "B", "text": "maximum height", "percentage": "6.11%", "isCorrect": False},
            {"id": "C", "text": "kinetic energy at highest point", "percentage": "5.15%", "isCorrect": False},
            {"id": "D", "text": "range of projectile", "percentage": "79.46%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "range of projectile",
        "accuracy": "79.46%",
        "accuracyPct": 79.46,
        "difficulty": "Easy",
        "solutionText": "Horizontal range is $R = \\frac{u^2 \\sin 2\\theta}{g}$. For complementary angles $\\theta_1$ and $\\theta_2 = 90^\\circ - \\theta_1$: $\\sin 2(90^\\circ - \\theta) = \\sin(180^\\circ - 2\\theta) = \\sin 2\\theta$. Since $60^\\circ + 30^\\circ = 90^\\circ$, $\\sin(2 \\times 60^\\circ) = \\sin 120^\\circ = \\sin 60^\\circ = \\sin(2 \\times 30^\\circ)$. Thus the horizontal range remains the same.",
        "videoSolutionUrl": "https://www.youtube.com/embed/Bq6k6j2vE7E",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_010",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Kinetic Energy of Projectile",
        "questionNumber": 10,
        "questionType": "Single Choice Question",
        "statement": "A body is projected with kinetic energy $K$ at an angle of $60^\\circ$ with the horizontal. Its kinetic energy at the highest point will be",
        "options": [
            {"id": "A", "text": "$K$", "percentage": "3.24%", "isCorrect": False},
            {"id": "B", "text": "$K/2$", "percentage": "5.24%", "isCorrect": False},
            {"id": "C", "text": "zero", "percentage": "3.1%", "isCorrect": False},
            {"id": "D", "text": "$K/4$", "percentage": "88.42%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "K/4",
        "accuracy": "88.42%",
        "accuracyPct": 88.42,
        "difficulty": "Easy",
        "solutionText": "Initial kinetic energy $K = \\frac{1}{2} m u^2$. At the highest point of projectile motion, the vertical velocity is zero ($v_y = 0$), so the velocity is solely horizontal: $v_x = u \\cos\\theta = u \\cos 60^\\circ = \\frac{u}{2}$. The kinetic energy at the top is $K' = \\frac{1}{2} m v_x^2 = \\frac{1}{2} m \\left(\\frac{u}{2}\\right)^2 = \\frac{1}{4}\\left(\\frac{1}{2} m u^2\\right) = \\frac{K}{4}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/qFv6sN7A2wY",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_011",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Maximum Range & Muzzle Velocity",
        "questionNumber": 11,
        "questionType": "Single Choice Question",
        "statement": "The maximum range of a gun on horizontal terrain is 16 km. If $g = 10\\text{ m/s}^2$, the muzzle velocity of the shell must be",
        "options": [
            {"id": "A", "text": "160 m/s", "percentage": "4.13%", "isCorrect": False},
            {"id": "B", "text": "200 m/s", "percentage": "5.1%", "isCorrect": False},
            {"id": "C", "text": "400 m/s", "percentage": "86.87%", "isCorrect": True},
            {"id": "D", "text": "$200\\sqrt{2}\\text{ m/s}$", "percentage": "3.9%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "400 m/s",
        "accuracy": "86.87%",
        "accuracyPct": 86.87,
        "difficulty": "Easy",
        "solutionText": "Maximum horizontal range occurs at $\\theta = 45^\\circ$ and is given by $R_{\\max} = \\frac{u^2}{g}$. Given $R_{\\max} = 16\\text{ km} = 16000\\text{ m}$ and $g = 10\\text{ m/s}^2$: $u^2 = R_{\\max} \\times g = 16000 \\times 10 = 160000\\text{ m}^2/\\text{s}^2 \\implies u = \\sqrt{160000} = 400\\text{ m/s}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/1v0fXvM0b9Q",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_012",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Relative Motion & Shortest Distance",
        "questionNumber": 12,
        "questionType": "Single Choice Question",
        "statement": "A ship A is moving Westwards with a speed of 10 km/h and a ship B 100 km South of A, is moving Northwards with a speed of 10 km/h. The time after which the distance between them becomes shortest is:",
        "options": [
            {"id": "A", "text": "5 h", "percentage": "31.94%", "isCorrect": True},
            {"id": "B", "text": "$5\\sqrt{2}\\text{ h}$", "percentage": "34.1%", "isCorrect": False},
            {"id": "C", "text": "$10\\sqrt{2}\\text{ h}$", "percentage": "25.17%", "isCorrect": False},
            {"id": "D", "text": "0 h", "percentage": "8.93%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "5 h",
        "accuracy": "31.94%",
        "accuracyPct": 31.94,
        "difficulty": "Medium",
        "solutionText": "Position of A at time $t$: $\\vec{r}_A = -10t\\hat{i}$. Position of B at time $t$: $\\vec{r}_B = (10t - 100)\\hat{j}$. Relative separation vector: $\\vec{r} = \\vec{r}_A - \\vec{r}_B = -10t\\hat{i} - (10t - 100)\\hat{j}$. Squared distance: $D^2 = (-10t)^2 + (100 - 10t)^2 = 100t^2 + 10000 - 2000t + 100t^2 = 200t^2 - 2000t + 10000$. To minimize distance, $\\frac{d(D^2)}{dt} = 400t - 2000 = 0 \\implies t = \\frac{2000}{400} = 5\\text{ h}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/wT95o-rwigc",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_013",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Rain-Man Problem",
        "questionNumber": 13,
        "questionType": "Single Choice Question",
        "statement": "To man running at a speed of 5 m/sec, the rain drops appear to be falling at an angle of $45^\\circ$ from the vertical. If the rain drops are actually falling vertically downwards, then velocity in m/sec is",
        "options": [
            {"id": "A", "text": "5", "percentage": "51.64%", "isCorrect": True},
            {"id": "B", "text": "$5\\sqrt{3}$", "percentage": "18.36%", "isCorrect": False},
            {"id": "C", "text": "$5\\sqrt{2}$", "percentage": "26.71%", "isCorrect": False},
            {"id": "D", "text": "4", "percentage": "3.34%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "5",
        "accuracy": "51.64%",
        "accuracyPct": 51.64,
        "difficulty": "Medium",
        "solutionText": "Let velocity of man be $\\vec{v}_m = 5\\hat{i}\\text{ m/s}$. Actual velocity of rain is $\\vec{v}_r = -v\\hat{j}\\text{ m/s}$. Velocity of rain relative to man is $\\vec{v}_{rm} = \\vec{v}_r - \\vec{v}_m = -5\\hat{i} - v\\hat{j}$. The angle with vertical is given by $\\tan 45^\\circ = \\frac{|v_{rm, x}|}{|v_{rm, y}|} = \\frac{5}{v}$. Since $\\tan 45^\\circ = 1$, we have $1 = \\frac{5}{v} \\implies v = 5\\text{ m/s}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/c8__GJIgK2A",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_014",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Projectile Assumptions",
        "questionNumber": 14,
        "questionType": "Single Choice Question",
        "statement": "For projectile motion, we will assume that the air resistance has ...X... effect on the motion of the projectile. Here, X refers to",
        "options": [
            {"id": "A", "text": "Sufficient", "percentage": "4.65%", "isCorrect": False},
            {"id": "B", "text": "Insufficient", "percentage": "2.33%", "isCorrect": False},
            {"id": "C", "text": "Negligible", "percentage": "90.7%", "isCorrect": True},
            {"id": "D", "text": "Proper", "percentage": "2.33%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "Negligible",
        "accuracy": "90.7%",
        "accuracyPct": 90.7,
        "difficulty": "Easy",
        "solutionText": "In standard Newtonian kinematics and projectile motion analysis in NCERT physics, air resistance is assumed to be negligible so that acceleration remains constant downwards ($g$) with zero horizontal acceleration.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_015",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "River-Swimmer Problem",
        "questionNumber": 15,
        "questionType": "Single Choice Question",
        "statement": "A river is flowing due east with a speed 3 ms$^{-1}$. A swimmer can swim in still water at a speed of 4 ms$^{-1}$. If swimmer starts swimming due north, then the resultant velocity of the swimmer is",
        "options": [
            {"id": "A", "text": "3 ms$^{-1}$", "percentage": "8%", "isCorrect": False},
            {"id": "B", "text": "5 ms$^{-1}$", "percentage": "38%", "isCorrect": True},
            {"id": "C", "text": "7 ms$^{-1}$", "percentage": "52%", "isCorrect": False},
            {"id": "D", "text": "2 ms$^{-1}$", "percentage": "2%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "5 ms^{-1}",
        "accuracy": "38%",
        "accuracyPct": 38.0,
        "difficulty": "Easy",
        "solutionText": "River velocity $\\vec{v}_r = 3\\hat{i}\\text{ ms}^{-1}$ (east). Swimmer velocity relative to water $\\vec{v}_{s/r} = 4\\hat{j}\\text{ ms}^{-1}$ (north). Resultant velocity of swimmer relative to ground is $\\vec{v} = \\vec{v}_{s/r} + \\vec{v}_r = 4\\hat{j} + 3\\hat{i}\\text{ ms}^{-1}$. Magnitude is $v = \\sqrt{4^2 + 3^2} = \\sqrt{16 + 9} = \\sqrt{25} = 5\\text{ ms}^{-1}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_016",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Obstacle Clearance in Projectile Motion",
        "questionNumber": 16,
        "questionType": "Multiple Choice Question",
        "statement": "At what angle should a body be projected with a velocity 24 ms$^{-1}$ just to pass over the obstacle 14 m high at a distance of 24 m . [Take $g = 10\\text{ ms}^{-2}$]",
        "options": [
            {"id": "A", "text": "$\\tan\\theta = 19 / 5$", "percentage": "65.9%", "isCorrect": True},
            {"id": "B", "text": "$\\tan\\theta = 1$", "percentage": "66%", "isCorrect": True},
            {"id": "C", "text": "$\\tan\\theta = 3$", "percentage": "18.25%", "isCorrect": False},
            {"id": "D", "text": "$\\tan\\theta = 2$", "percentage": "12.32%", "isCorrect": False}
        ],
        "correctOption": "A, B",
        "correctAnswer": "\\tan\\theta = 19/5, \\tan\\theta = 1",
        "accuracy": "51.34%",
        "accuracyPct": 51.34,
        "difficulty": "Hard",
        "solutionText": "Equation of trajectory of projectile is $y = x\\tan\\theta - \\frac{g x^2}{2 u^2 \\cos^2\\theta} = x\\tan\\theta - \\frac{g x^2(1 + \\tan^2\\theta)}{2 u^2}$. Substituting $y = 14\\text{ m}$, $x = 24\\text{ m}$, $u = 24\\text{ ms}^{-1}$, $g = 10\\text{ ms}^{-2}$:\n$14 = 24\\tan\\theta - \\frac{10 \\times (24)^2 (1 + \\tan^2\\theta)}{2 \\times 24^2} = 24\\tan\\theta - 5(1 + \\tan^2\\theta)$.\nRearranging gives quadratic in $\\tan\\theta$: $5\\tan^2\\theta - 24\\tan\\theta + 19 = 0$.\nFactoring: $(5\\tan\\theta - 19)(\\tan\\theta - 1) = 0 \\implies \\tan\\theta = 1$ or $\\tan\\theta = \\frac{19}{5}$. Both options A and B are correct.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_017",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Relative Motion & Shortest Distance",
        "questionNumber": 17,
        "questionType": "Single Choice Question",
        "statement": "A ship A is moving Westwards with a speed of 10 km/h and a ship B 100 km South of A, is moving Northwards with a speed of 10 km/h. The time after which the distance between them becomes shortest, is :-",
        "options": [
            {"id": "A", "text": "5 h", "percentage": "54.75%", "isCorrect": True},
            {"id": "B", "text": "$5\\sqrt{2}\\text{ h}$", "percentage": "22.54%", "isCorrect": False},
            {"id": "C", "text": "$10\\sqrt{2}\\text{ h}$", "percentage": "18.32%", "isCorrect": False},
            {"id": "D", "text": "0 h", "percentage": "4.43%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "5 h",
        "accuracy": "54.75%",
        "accuracyPct": 54.75,
        "difficulty": "Medium",
        "solutionText": "Position vectors: $\\vec{r}_A = -10t\\hat{i}$, $\\vec{r}_B = (10t - 100)\\hat{j}$. Relative separation vector: $\\vec{r}_{A/B} = -10t\\hat{i} - (10t - 100)\\hat{j}$. Distance squared: $r^2 = 100t^2 + (100 - 10t)^2 = 200t^2 - 2000t + 10000$. Differentiating and setting to zero: $\\frac{d(r^2)}{dt} = 400t - 2000 = 0 \\implies t = 5\\text{ h}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/wT95o-rwigc",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_018",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Gravitational Acceleration Scaling",
        "questionNumber": 18,
        "questionType": "Single Choice Question",
        "statement": "A projectile thrown with a speed V at an angle $\\theta$ has a range R on the surface of earth. For same V and $\\theta$, its range on the surface of moon will be",
        "options": [
            {"id": "A", "text": "R/6", "percentage": "16.67%", "isCorrect": False},
            {"id": "B", "text": "6R", "percentage": "75%", "isCorrect": True},
            {"id": "C", "text": "R/36", "percentage": "8.33%", "isCorrect": False},
            {"id": "D", "text": "36R", "percentage": "0%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "6R",
        "accuracy": "75%",
        "accuracyPct": 75.0,
        "difficulty": "Easy",
        "solutionText": "Horizontal range is $R = \\frac{V^2 \\sin 2\\theta}{g}$. Since $V$ and $\\theta$ are identical, $R \\propto \\frac{1}{g}$. On the moon, surface gravity is $g_m = \\frac{g_e}{6}$. Therefore, $R_m = \\frac{V^2 \\sin 2\\theta}{g_e / 6} = 6 \\left(\\frac{V^2 \\sin 2\\theta}{g_e}\\right) = 6R$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/d-Ihm2wcgjg",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_019",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Vertical Projection from Tower",
        "questionNumber": 19,
        "questionType": "Single Choice Question",
        "statement": "From a tower of height H, a particle is thrown vertically upwards with a speed u. The time taken by the particle, to hit the ground, is n times that taken by it to reach the highest point of its path. The relation between H, u and n is",
        "options": [
            {"id": "A", "text": "$2gH = n^2 u^2$", "percentage": "15.14%", "isCorrect": False},
            {"id": "B", "text": "$gH = (n - 2)^2 u^2 d$", "percentage": "17.93%", "isCorrect": False},
            {"id": "C", "text": "$2gH = n u^2 (n - 2)$", "percentage": "61.3%", "isCorrect": True},
            {"id": "D", "text": "$gH = (n - 2) u^2$", "percentage": "5.73%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "2gH = nu^2(n - 2)",
        "accuracy": "61.3%",
        "accuracyPct": 61.3,
        "difficulty": "Medium",
        "solutionText": "Time to reach highest point: $t_1 = \\frac{u}{g}$. Total time to hit ground: $t = n t_1 = \\frac{nu}{g}$. Using kinematic equation $-H = ut - \\frac{1}{2}gt^2$: $-H = u\\left(\\frac{nu}{g}\\right) - \\frac{1}{2}g\\left(\\frac{n^2 u^2}{g^2}\\right) = \\frac{nu^2}{g} - \\frac{n^2 u^2}{2g} = \\frac{nu^2(2 - n)}{2g} = -\\frac{nu^2(n - 2)}{2g}$. Multiplying by $-2g$: $2gH = nu^2(n - 2)$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/uRJ8gW8k4bA",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_020",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Projectile with Horizontal Retardation",
        "questionNumber": 20,
        "questionType": "Single Choice Question",
        "statement": "A ball is projected as shown in figure with velocity $u$ at angle $\theta$. If horizontal wind produces a constant deceleration $a_x = g\\cot\\theta$ and vertical downward acceleration is $g$, the ball will return to point :",
        "options": [
            {"id": "A", "text": "O", "percentage": "59.07%", "isCorrect": True},
            {"id": "B", "text": "left to point O", "percentage": "19.6%", "isCorrect": False},
            {"id": "C", "text": "right to point O", "percentage": "18.59%", "isCorrect": False},
            {"id": "D", "text": "none of these", "percentage": "2.77%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "O",
        "accuracy": "59.07%",
        "accuracyPct": 59.07,
        "difficulty": "Hard",
        "solutionText": "Time of flight is determined by vertical motion: $T = \\frac{2u_y}{g} = \\frac{2u\\sin\\theta}{g}$. Horizontal displacement during time $T$ under constant retardation $a_x = g\\cot\\theta$: $x = u_x T - \\frac{1}{2} a_x T^2 = (u\\cos\\theta)\\left(\\frac{2u\\sin\\theta}{g}\\right) - \\frac{1}{2}(g\\cot\\theta)\\left(\\frac{4u^2\\sin^2\\theta}{g^2}\\right) = \\frac{2u^2\\sin\\theta\\cos\\theta}{g} - \\frac{2u^2\\cos\\theta\\sin\\theta}{g} = 0$. Since horizontal displacement is zero when it lands, the ball lands exactly at origin O.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    }
]

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

print(f"Existing questions in pw_extracted_master.json: {len(master)}")

# Check if any ID already exists
existing_ids = {q.get('id') for q in master if q.get('id')}
added = 0
for q in new_questions:
    if q['id'] not in existing_ids:
        master.append(q)
        existing_ids.add(q['id'])
        added += 1

with open('pw_extracted_master.json', 'w', encoding='utf-8') as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Added {added} questions. Total in pw_extracted_master.json: {len(master)}")
