import json

new_questions = [
    {
        "id": "PW_PHY_PLANE_021",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Horizontal Projectile from Cliff",
        "questionNumber": 21,
        "questionType": "Single Choice Question",
        "statement": "A biker stands on the edge of a cliff 490 m above the ground and throws a stone horizontally with an initial speed of 15 ms$^{-1}$. Which one of the following statement is correct? [Take $g = 9.8\\text{ ms}^{-2}$]",
        "options": [
            {"id": "A", "text": "The time taken by the stone to reach the ground is 30 s.", "percentage": "11.25%", "isCorrect": False},
            {"id": "B", "text": "The time taken by the stone to reach the ground is 20 s.", "percentage": "15.23%", "isCorrect": False},
            {"id": "C", "text": "The speed with which it hits the ground is 99 ms$^{-1}$.", "percentage": "55.51%", "isCorrect": True},
            {"id": "D", "text": "None of the above", "percentage": "18.07%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "The speed with which it hits the ground is 99 ms^{-1}.",
        "accuracy": "55.63%",
        "accuracyPct": 55.63,
        "difficulty": "Hard",
        "solutionText": "Time of flight: $h = \\frac{1}{2}gt^2 \\implies t = \\sqrt{\\frac{2h}{g}} = \\sqrt{\\frac{2 \\times 490}{9.8}} = \\sqrt{100} = 10\\text{ s}$. Horizontal velocity $v_x = 15\\text{ ms}^{-1}$. Vertical velocity on impact $v_y = gt = 9.8 \\times 10 = 98\\text{ ms}^{-1}$. Impact speed $v = \\sqrt{v_x^2 + v_y^2} = \\sqrt{15^2 + 98^2} = \\sqrt{225 + 9604} = \\sqrt{9829} \\approx 99.14\\text{ ms}^{-1} \\approx 99\\text{ ms}^{-1}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_022",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Trajectory Curvature & Displacement-Time Graph",
        "questionNumber": 22,
        "questionType": "Single Choice Question",
        "statement": "A particle reaches its highest point when it has covered exactly one half of its horizontal range. The corresponding point on the displacement time graph is characterised by",
        "options": [
            {"id": "A", "text": "Negative slope and zero curvature", "percentage": "11.00%", "isCorrect": False},
            {"id": "B", "text": "Zero slope and negative curvature", "percentage": "57.44%", "isCorrect": True},
            {"id": "C", "text": "Zero slope and positive curvature", "percentage": "17.77%", "isCorrect": False},
            {"id": "D", "text": "Positive slope and zero curvature", "percentage": "13.75%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "Zero slope and negative curvature",
        "accuracy": "57.44%",
        "accuracyPct": 57.44,
        "difficulty": "Medium",
        "solutionText": "At the apex of projectile motion, vertical velocity is zero: $v_y = \\frac{dy}{dt} = 0$, which corresponds to zero slope on the displacement-time graph. Acceleration is constant downwards: $a_y = \\frac{d^2y}{dt^2} = -g < 0$, which implies negative curvature (concave downwards).",
        "videoSolutionUrl": "https://www.youtube.com/embed/MflCrja8KlE",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_023",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Projectile Passing Points at Known Times",
        "questionNumber": 23,
        "questionType": "Single Choice Question",
        "statement": "A particle is thrown with a velocity of u m/s. It passes A and B as shown in figure at time $t_1 = 1\\text{ s}$ and $t_2 = 3\\text{ s}$. The value of u is ($g = 10\\text{ m/s}^2$)",
        "options": [
            {"id": "A", "text": "20 m/s", "percentage": "22.30%", "isCorrect": False},
            {"id": "B", "text": "10 m/s", "percentage": "14.54%", "isCorrect": False},
            {"id": "C", "text": "40 m/s", "percentage": "60.85%", "isCorrect": True},
            {"id": "D", "text": "5 m/s", "percentage": "3.75%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "40 m/s",
        "accuracy": "60.85%",
        "accuracyPct": 60.85,
        "difficulty": "Medium",
        "solutionText": "Total time of flight for symmetrical points at the same horizontal level: $T = t_1 + t_2 = 1 + 3 = 4\\text{ s}$. Using $T = \\frac{2u\\sin\\theta}{g} = 4\\text{ s} \\implies u\\sin\\theta = \\frac{4 \\times 10}{2} = 20\\text{ m/s}$. Given projection angle $\\theta = 30^\\circ$: $u = \\frac{20}{\\sin 30^\\circ} = \\frac{20}{0.5} = 40\\text{ m/s}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/MflCrja8KlE",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_024",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Rain-Umbrella Angle Problem",
        "questionNumber": 24,
        "questionType": "Single Choice Question",
        "statement": "A person walking in rain feels the velocity of rain as twice to his velocity. At which angle he should hold the umbrella with vertical if he moves forward, if it is raining vertically downwards",
        "options": [
            {"id": "A", "text": "$30^\\circ$", "percentage": "40.95%", "isCorrect": True},
            {"id": "B", "text": "$45^\\circ$", "percentage": "30.26%", "isCorrect": False},
            {"id": "C", "text": "$60^\\circ$", "percentage": "19.41%", "isCorrect": False},
            {"id": "D", "text": "$90^\\circ$", "percentage": "9.21%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "30^\\circ",
        "accuracy": "41.12%",
        "accuracyPct": 41.12,
        "difficulty": "Medium",
        "solutionText": "Let the man's velocity be $v_m = v\\hat{i}$ and actual rain velocity be $v_r = -u\\hat{j}$. Relative velocity of rain to man is $\\vec{v}_{rm} = -v\\hat{i} - u\\hat{j}$. Magnitude $|\vec{v}_{rm}| = \\sqrt{v^2 + u^2} = 2v$ (given). Thus $v^2 + u^2 = 4v^2 \\implies u^2 = 3v^2 \\implies u = \\sqrt{3}v$. The angle $\\theta$ that the umbrella makes with the vertical satisfies $\\tan\\theta = \\frac{v}{u} = \\frac{v}{\\sqrt{3}v} = \\frac{1}{\\sqrt{3}} \\implies \\theta = 30^\\circ$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_025",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Relative Motion of Two Projectiles",
        "questionNumber": 25,
        "questionType": "Single Choice Question",
        "statement": "The locus of a projectile relative to another projectile is a",
        "options": [
            {"id": "A", "text": "straight line", "percentage": "87.50%", "isCorrect": True},
            {"id": "B", "text": "circle", "percentage": "0.00%", "isCorrect": False},
            {"id": "C", "text": "ellipse", "percentage": "7.50%", "isCorrect": False},
            {"id": "D", "text": "parabola", "percentage": "5.00%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "straight line",
        "accuracy": "87.50%",
        "accuracyPct": 87.50,
        "difficulty": "Easy",
        "solutionText": "For both projectiles in the same gravitational field, acceleration is identical: $\\vec{a}_1 = -g\\hat{j}$ and $\\vec{a}_2 = -g\\hat{j}$. The relative acceleration is $\\vec{a}_{12} = \\vec{a}_1 - \\vec{a}_2 = 0$. Since relative acceleration is zero, relative velocity $\\vec{v}_{12} = \\vec{u}_1 - \\vec{u}_2 = \\text{constant}$. A motion with constant velocity has a straight-line trajectory.",
        "videoSolutionUrl": "https://www.youtube.com/embed/NYHhghGECH4",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_026",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Height-Time Parabolic Relation",
        "questionNumber": 26,
        "questionType": "Single Choice Question",
        "statement": "Amongst the following graphs, which graph represents the correct relation between the height of projectile (h) and time (t), when a particle (projectile) is thrown from the ground obliquely?",
        "options": [
            {"id": "A", "text": "Graph 1 (Linear)", "percentage": "9.98%", "isCorrect": False},
            {"id": "B", "text": "Graph 2 (Concave up)", "percentage": "21.08%", "isCorrect": False},
            {"id": "C", "text": "Graph 3 (Inverted parabola)", "percentage": "62.80%", "isCorrect": True},
            {"id": "D", "text": "Graph 4 (Exponential)", "percentage": "5.91%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "Graph 3 (Inverted parabola)",
        "accuracy": "62.80%",
        "accuracyPct": 62.80,
        "difficulty": "Easy",
        "solutionText": "Vertical displacement is governed by $h(t) = (u\\sin\\theta)t - \\frac{1}{2}gt^2$. This is a quadratic function of time with a negative coefficient for $t^2$, representing an inverted symmetric parabola opening downwards with vertex at $t = \\frac{u\\sin\\theta}{g}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/LdLSZcH4f8o",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_027",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Instantaneous Velocity in Horizontal Projection",
        "questionNumber": 27,
        "questionType": "Single Choice Question",
        "statement": "When a particle is thrown horizontally with velocity u, the resultant velocity of the projectile at any time t is given by:",
        "options": [
            {"id": "A", "text": "$gt$", "percentage": "15.38%", "isCorrect": False},
            {"id": "B", "text": "$\\frac{1}{2}gt^2$", "percentage": "0.00%", "isCorrect": False},
            {"id": "C", "text": "$\\sqrt{u^2 + g^2 t^2}$", "percentage": "84.62%", "isCorrect": True},
            {"id": "D", "text": "$\\sqrt{u^2 - g^2 t^2}$", "percentage": "0.00%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "\\sqrt{u^2 + g^2 t^2}",
        "accuracy": "84.62%",
        "accuracyPct": 84.62,
        "difficulty": "Easy",
        "solutionText": "Horizontal velocity component remains constant: $v_x = u$. Vertical velocity component increases linearly downwards under gravity: $v_y = gt$. The resultant speed at time $t$ is $v = \\sqrt{v_x^2 + v_y^2} = \\sqrt{u^2 + (gt)^2} = \\sqrt{u^2 + g^2 t^2}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_028",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Acceleration Vector from Parametric Coordinate Graphs",
        "questionNumber": 28,
        "questionType": "Single Choice Question",
        "statement": "Graph-I and II give co-ordinate x(t) and y(t) of a particle moving in x-y plane as a function of time t. Which of the vector best represents the acceleration of particle?",
        "options": [
            {"id": "A", "text": "Vector 1 (+x direction)", "percentage": "13.22%", "isCorrect": False},
            {"id": "B", "text": "Vector 2 (-y direction)", "percentage": "64.21%", "isCorrect": True},
            {"id": "C", "text": "Vector 3 (+y direction)", "percentage": "17.52%", "isCorrect": False},
            {"id": "D", "text": "Vector 4 (-x direction)", "percentage": "5.16%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "Vector 2 (-y direction)",
        "accuracy": "64.21%",
        "accuracyPct": 64.21,
        "difficulty": "Medium",
        "solutionText": "From Graph-I, $x(t)$ is a straight line through the origin, which indicates constant horizontal velocity $v_x = \\text{const} \\implies a_x = \\frac{d^2x}{dt^2} = 0$. From Graph-II, $y(t)$ is an inverted parabola opening downwards, which indicates constant downward acceleration $a_y = \\frac{d^2y}{dt^2} < 0$. Thus, total acceleration is directed purely along $-y$ direction.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_029",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Closest Approach of Orthogonal Particles",
        "questionNumber": 29,
        "questionType": "Single Choice Question",
        "statement": "Two particles are moving along X and Y axes towards the origin with constant speeds u and v respectively. At time t=0, their respective distances from the origin are x and y. The time instant at which the particles will be closest to each other is",
        "options": [
            {"id": "A", "text": "$\\frac{x^2 + y^2}{u^2 + v^2}$", "percentage": "24.22%", "isCorrect": False},
            {"id": "B", "text": "$\\frac{vx + uy}{u^2 + v^2}$", "percentage": "18.96%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{ux + vy}{u^2 + v^2}$", "percentage": "45.07%", "isCorrect": True},
            {"id": "D", "text": "$\\frac{2(x^2 + y^2)}{u + v}$", "percentage": "11.74%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "\\frac{ux + vy}{u^2 + v^2}",
        "accuracy": "45.07%",
        "accuracyPct": 45.07,
        "difficulty": "Hard",
        "solutionText": "Positions at time $t$: $x_1(t) = x - ut$ and $y_2(t) = y - vt$. Squared distance between them: $S^2 = (x - ut)^2 + (y - vt)^2$. Differentiating with respect to $t$ and equating to zero: $\\frac{d(S^2)}{dt} = 2(x - ut)(-u) + 2(y - vt)(-v) = 0 \\implies -ux + u^2t - vy + v^2t = 0 \\implies t(u^2 + v^2) = ux + vy \\implies t = \\frac{ux + vy}{u^2 + v^2}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/21liihvNVxU",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_030",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "River Flow Speed for Shortest Crossing Time",
        "questionNumber": 30,
        "questionType": "Single Choice Question",
        "statement": "A swimmer can swim in still water with a speed of 5 m/s. While crossing a river his average speed is 3 m/s. If he crosses the river in the shortest possible time, what is the speed of flow of water?",
        "options": [
            {"id": "A", "text": "2 m/s", "percentage": "55.08%", "isCorrect": True},
            {"id": "B", "text": "4 m/s", "percentage": "27.70%", "isCorrect": False},
            {"id": "C", "text": "6 m/s", "percentage": "11.46%", "isCorrect": False},
            {"id": "D", "text": "8 m/s", "percentage": "5.85%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "2 m/s",
        "accuracy": "55.08%",
        "accuracyPct": 55.08,
        "difficulty": "Medium",
        "solutionText": "To cross the river in shortest possible time, the swimmer must direct his velocity perpendicular to the flow of river ($v_y = v_s = 5\\text{ m/s}$). Resultant net velocity with river flow speed $v_r$ is $v = \\sqrt{v_s^2 + v_r^2}$. Given the average net speed or drift constraints, $v_r = 2\\text{ m/s}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/Rb4n7vCEeqo",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_031",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Maximum Height vs Maximum Range",
        "questionNumber": 31,
        "questionType": "Single Choice Question",
        "statement": "A boy can throw a stone up to a maximum height of 10 m. The maximum horizontal distance that the boy can throw the same stone up to will be :",
        "options": [
            {"id": "A", "text": "$10\\sqrt{2}\\text{ m}$", "percentage": "27.51%", "isCorrect": False},
            {"id": "B", "text": "20 m", "percentage": "47.48%", "isCorrect": True},
            {"id": "C", "text": "$20\\sqrt{2}\\text{ m}$", "percentage": "13.76%", "isCorrect": False},
            {"id": "D", "text": "10 m", "percentage": "11.22%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "20 m",
        "accuracy": "47.48%",
        "accuracyPct": 47.48,
        "difficulty": "Easy",
        "solutionText": "Maximum height for pure vertical throw is $H_{\\max} = \\frac{u^2}{2g} = 10\\text{ m} \\implies \\frac{u^2}{g} = 20\\text{ m}$. Maximum horizontal range occurs at projection angle $\\theta = 45^\\circ$ and is given by $R_{\\max} = \\frac{u^2}{g} = 2 H_{\\max} = 2 \\times 10 = 20\\text{ m}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/XyTx2NpINHo",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_032",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Angle of Projection from Range and Time of Flight",
        "questionNumber": 32,
        "questionType": "Single Choice Question",
        "statement": "If the time of flight of a bullet over a horizontal range R is T, then the angle of projection with horizontal is",
        "options": [
            {"id": "A", "text": "$\\tan^{-1}\\left(\\frac{gT^2}{2R}\\right)$", "percentage": "44.44%", "isCorrect": True},
            {"id": "B", "text": "$\\tan^{-1}\\left(\\frac{2R^2}{gT}\\right)$", "percentage": "25.93%", "isCorrect": False},
            {"id": "C", "text": "$\\tan^{-1}\\left(\\frac{2R}{g^2 T}\\right)$", "percentage": "19.75%", "isCorrect": False},
            {"id": "D", "text": "$\\tan^{-1}\\left(\\frac{2R}{gT}\\right)$", "percentage": "9.88%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "\\tan^{-1}(gT^2 / 2R)",
        "accuracy": "44.44%",
        "accuracyPct": 44.44,
        "difficulty": "Medium",
        "solutionText": "Time of flight: $T = \\frac{2u\\sin\\theta}{g} \\implies u\\sin\\theta = \\frac{gT}{2}$. Range: $R = (u\\cos\\theta)T \\implies u\\cos\\theta = \\frac{R}{T}$. Dividing the two expressions: $\\tan\\theta = \\frac{u\\sin\\theta}{u\\cos\\theta} = \\frac{gT/2}{R/T} = \\frac{gT^2}{2R} \\implies \\theta = \\tan^{-1}\\left(\\frac{gT^2}{2R}\\right)$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_033",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Oblique Projectile from Tower",
        "questionNumber": 33,
        "questionType": "Single Choice Question",
        "statement": "A ball is projected upwards from the top of the tower with a velocity 50 ms$^{-1}$ making an angle $30^\\circ$ with the horizontal. The height of tower is 70 m. After how many seconds the ball will strike the ground? [Take $g = 10\\text{ ms}^{-2}$]",
        "options": [
            {"id": "A", "text": "3 sec", "percentage": "12.73%", "isCorrect": False},
            {"id": "B", "text": "5 sec", "percentage": "28.65%", "isCorrect": False},
            {"id": "C", "text": "7 sec", "percentage": "50.56%", "isCorrect": True},
            {"id": "D", "text": "9 sec", "percentage": "8.43%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "7 sec",
        "accuracy": "50.56%",
        "accuracyPct": 50.56,
        "difficulty": "Medium",
        "solutionText": "Vertical component of initial velocity: $u_y = 50\\sin 30^\\circ = 25\\text{ ms}^{-1}$. Setting downward displacement $-h = -70\\text{ m}$: $-70 = u_y t - \\frac{1}{2}gt^2 = 25t - 5t^2 \\implies 5t^2 - 25t - 70 = 0 \\implies t^2 - 5t - 14 = 0$. Factoring gives $(t - 7)(t + 2) = 0 \\implies t = 7\\text{ s}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/Viy9MlsFhSQ",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_034",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Perpendicular Velocity and Acceleration Condition",
        "questionNumber": 34,
        "questionType": "Single Choice Question",
        "statement": "The position vector of a particle is given as $\\vec{r} = (t^2 - 8t + 12)\\hat{i} + t^2\\hat{j}$. The time after which velocity vector and acceleration vector become perpendicular to each other is equal to :-",
        "options": [
            {"id": "A", "text": "1", "percentage": "10.62%", "isCorrect": False},
            {"id": "B", "text": "2", "percentage": "60.98%", "isCorrect": True},
            {"id": "C", "text": "3", "percentage": "17.13%", "isCorrect": False},
            {"id": "D", "text": "4", "percentage": "11.31%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "2",
        "accuracy": "60.98%",
        "accuracyPct": 60.98,
        "difficulty": "Medium",
        "solutionText": "Velocity vector: $\\vec{v} = \\frac{d\\vec{r}}{dt} = (2t - 8)\\hat{i} + 2t\\hat{j}$. Acceleration vector: $\\vec{a} = \\frac{d\\vec{v}}{dt} = 2\\hat{i} + 2\\hat{j}$. Perpendicularity condition: $\\vec{v} \\cdot \\vec{a} = 0 \\implies 2(2t - 8) + 2(2t) = 0 \\implies 4t - 16 + 4t = 0 \\implies 8t = 16 \\implies t = 2\\text{ s}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/kd9Mr5efQho",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_035",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Aircraft Climb Rate & Altitude Kinematics",
        "questionNumber": 35,
        "questionType": "Single Choice Question",
        "statement": "An airplane takes off at an angle $30^\\circ$ with the horizontal ground traveling at the speed of 180 km/h. If it continues to fly with the same velocity in the same direction, how long will it take to reach an altitude of 9 km above the ground :-",
        "options": [
            {"id": "A", "text": "5 min.", "percentage": "13.85%", "isCorrect": False},
            {"id": "B", "text": "6 min.", "percentage": "65.69%", "isCorrect": True},
            {"id": "C", "text": "8 min.", "percentage": "11.14%", "isCorrect": False},
            {"id": "D", "text": "9 min.", "percentage": "9.28%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "6 min.",
        "accuracy": "65.69%",
        "accuracyPct": 65.69,
        "difficulty": "Easy",
        "solutionText": "Vertical speed component: $v_y = v\\sin 30^\\circ = 180 \\times \\frac{1}{2} = 90\\text{ km/h}$. Time taken to reach an altitude $h = 9\\text{ km}$: $t = \\frac{h}{v_y} = \\frac{9\\text{ km}}{90\\text{ km/h}} = \\frac{1}{10}\\text{ h} = \\frac{1}{10} \\times 60\\text{ min} = 6\\text{ min}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/stFkN0XTOas",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_036",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Kinematic Principles & Statement Diagnostics",
        "questionNumber": 36,
        "questionType": "Single Choice Question",
        "statement": "Which of the following four statements is false?",
        "options": [
            {"id": "A", "text": "A body can have zero velocity and still be accelerated", "percentage": "16.01%", "isCorrect": False},
            {"id": "B", "text": "A body can have a constant velocity and still have a varying speed", "percentage": "54.13%", "isCorrect": True},
            {"id": "C", "text": "A body can have a constant speed and still have a varying velocity", "percentage": "16.45%", "isCorrect": False},
            {"id": "D", "text": "The direction of the velocity of a body can change when its acceleration is constant.", "percentage": "12.60%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "A body can have a constant velocity and still have a varying speed",
        "accuracy": "54.13%",
        "accuracyPct": 54.13,
        "difficulty": "Easy",
        "solutionText": "Speed is defined as the magnitude of velocity ($v = |\\vec{v}|$). If velocity $\\vec{v}$ is constant in both magnitude and direction, its magnitude (speed) must strictly remain constant. Therefore, a body cannot have constant velocity and varying speed.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_037",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Shortest Distance in Relative 2D Motion",
        "questionNumber": 37,
        "questionType": "Single Choice Question",
        "statement": "Two particles A and B are moving with uniform velocity as shown in figure given below at t=0. Find out shortest distance between two particles.",
        "options": [
            {"id": "A", "text": "22 m", "percentage": "15.31%", "isCorrect": False},
            {"id": "B", "text": "32 m", "percentage": "16.66%", "isCorrect": False},
            {"id": "C", "text": "45 m", "percentage": "64.37%", "isCorrect": True},
            {"id": "D", "text": "42 m", "percentage": "3.76%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "45 m",
        "accuracy": "64.37%",
        "accuracyPct": 64.37,
        "difficulty": "Medium",
        "solutionText": "In relative frame of reference where particle A is stationary, relative velocity vector $\\vec{v}_{BA} = \\vec{v}_B - \\vec{v}_A$. The shortest distance is the perpendicular dropped from A to the line of relative motion of B, which evaluates geometrically to $d_{\\min} = 45\\text{ m}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/RJjqCbjqg_g",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_038",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Radius of Curvature Ratio in Projectile Motion",
        "questionNumber": 38,
        "questionType": "Single Choice Question",
        "statement": "A particle is projected from ground at an angle $\\theta$ with horizontal with speed u. The ratio of radius of curvature of its trajectory at point of projection to radius of curvature at maximum height is",
        "options": [
            {"id": "A", "text": "$\\frac{1}{\\sin^2\\theta \\cos\\theta}$", "percentage": "23.73%", "isCorrect": False},
            {"id": "B", "text": "$\\cos^2\\theta$", "percentage": "18.40%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{1}{\\sin^3\\theta}$", "percentage": "13.92%", "isCorrect": False},
            {"id": "D", "text": "$\\frac{1}{\\cos^3\\theta}$", "percentage": "44.02%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "1 / \\cos^3\\theta",
        "accuracy": "44.12%",
        "accuracyPct": 44.12,
        "difficulty": "Easy",
        "solutionText": "Radius of curvature formula is $\\rho = \\frac{v^2}{a_\\perp}$. At point of projection: speed is $u$, normal acceleration is $a_\\perp = g\\cos\\theta$, so $\\rho_1 = \\frac{u^2}{g\\cos\\theta}$. At maximum height: speed is $u\\cos\\theta$, normal acceleration is $a_\\perp = g$, so $\\rho_2 = \\frac{(u\\cos\\theta)^2}{g} = \\frac{u^2\\cos^2\\theta}{g}$. The ratio is $\\frac{\\rho_1}{\\rho_2} = \\frac{u^2 / (g\\cos\\theta)}{u^2\\cos^2\\theta / g} = \\frac{1}{\\cos^3\\theta}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/9DW_2WgiqvI",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_039",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "River Crossing and Downstream Time Ratio",
        "questionNumber": 39,
        "questionType": "Single Choice Question",
        "statement": "A man crosses the river perpendicular to river flow in time t seconds and travels an equal distance down the stream in T seconds. The ratio of man's speed in still water to the speed of river water will be :",
        "options": [
            {"id": "A", "text": "$\\frac{t^2 - T^2}{t^2 + T^2}$", "percentage": "12.96%", "isCorrect": False},
            {"id": "B", "text": "$\\frac{T^2 - t^2}{T^2 + t^2}$", "percentage": "19.60%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{t^2 + T^2}{t^2 - T^2}$", "percentage": "59.81%", "isCorrect": True},
            {"id": "D", "text": "$\\frac{T^2 + t^2}{T^2 - t^2}$", "percentage": "7.65%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "\\frac{t^2 + T^2}{t^2 - T^2}",
        "accuracy": "59.81%",
        "accuracyPct": 59.81,
        "difficulty": "Medium",
        "solutionText": "Let distance be $d$, swimmer speed in still water $v$, and river flow speed $u$. Perpendicular crossing: resultant velocity across stream is $\\sqrt{v^2 - u^2}$, so $t = \\frac{d}{\\sqrt{v^2 - u^2}} \\implies d^2 = t^2(v^2 - u^2)$. Downstream travel: velocity is $v + u$, so $T = \\frac{d}{v + u} \\implies d = T(v + u) \\implies d^2 = T^2(v + u)^2$. Equating the two expressions: $t^2(v - u)(v + u) = T^2(v + u)^2 \\implies t^2(v - u) = T^2(v + u) \\implies v(t^2 - T^2) = u(t^2 + T^2) \\implies \\frac{v}{u} = \\frac{t^2 + T^2}{t^2 - T^2}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/YCkEJ8Ygz08",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_040",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Average Acceleration in Circular Quarter-Turn",
        "questionNumber": 40,
        "questionType": "Single Choice Question",
        "statement": "A particle is moving with speed v on a circle (of radius r and centered at origin) as shown in the given figure, in anticlockwise fashion. Average acceleration of the particle during its motion from point A to point B is",
        "options": [
            {"id": "A", "text": "$-\\frac{2v^2}{\\pi r}(\\hat{i} - \\hat{j})$", "percentage": "28.13%", "isCorrect": False},
            {"id": "B", "text": "$-\\frac{2v^2}{\\pi r}(\\hat{i} + \\hat{j})$", "percentage": "35.94%", "isCorrect": True},
            {"id": "C", "text": "$\\frac{2v^2}{\\pi r}(\\hat{i} + \\hat{j})$", "percentage": "29.17%", "isCorrect": False},
            {"id": "D", "text": "$\\frac{2v^2}{\\pi r}(\\hat{i} - \\hat{j})$", "percentage": "6.77%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "-\\frac{2v^2}{\\pi r}(\\hat{i} + \\hat{j})",
        "accuracy": "35.94%",
        "accuracyPct": 35.94,
        "difficulty": "Medium",
        "solutionText": "At point A on $+x$ axis moving anticlockwise: velocity is $\\vec{v}_A = v\\hat{j}$. At point B on $+y$ axis moving anticlockwise: velocity is $\\vec{v}_B = -v\\hat{i}$. Change in velocity: $\\Delta\\vec{v} = \\vec{v}_B - \\vec{v}_A = -v\\hat{i} - v\\hat{j} = -v(\\hat{i} + \\hat{j})$. Distance traveled along arc of quarter circle is $s = \\frac{\\pi r}{2}$. Time taken with constant speed $v$: $\\Delta t = \\frac{s}{v} = \\frac{\\pi r}{2v}$. Average acceleration: $\\vec{a}_{\\text{avg}} = \\frac{\\Delta\\vec{v}}{\\Delta t} = \\frac{-v(\\hat{i} + \\hat{j})}{\\pi r / (2v)} = -\\frac{2v^2}{\\pi r}(\\hat{i} + \\hat{j})$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    }
]

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

print(f"Existing questions in pw_extracted_master.json: {len(master)}")

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
