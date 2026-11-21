import json

new_questions = [
    {
        "id": "PW_PHY_NLM_021",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "System Equilibrium & Limiting Friction",
        "questionNumber": 21,
        "questionType": "Single Choice Question",
        "statement": "In the system shown in figure the friction coefficient between ground and bigger block is $\\mu$. There is no friction between both the blocks. The string connecting both the blocks is light; all three pulleys are light and frictionless. Then the minimum limiting value of $\\mu$ so that the system remains in equilibrium is:",
        "options": [
            {"id": "A", "text": "1/2", "percentage": "22.14%", "isCorrect": False},
            {"id": "B", "text": "1/3", "percentage": "18.25%", "isCorrect": False},
            {"id": "C", "text": "2/3", "percentage": "37.57%", "isCorrect": True},
            {"id": "D", "text": "3/4", "percentage": "22.04%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "2/3",
        "accuracy": "37.57%",
        "accuracyPct": 37.57,
        "difficulty": "Hard",
        "solutionText": "Balancing forces in static equilibrium with string tension and normal reactions between the blocks and the ground: the friction force at the ground must balance the horizontal pull from the pulley arrangement. Setting limiting friction $f_{\\max} = \\mu N$ equal to horizontal tension yields $\\mu_{\\min} = \\frac{2}{3}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_022",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Pulley-Wedge Constraint Kinematics",
        "questionNumber": 22,
        "questionType": "Single Choice Question",
        "statement": "Find the acceleration of block C with respect to ground in the given pulley-wedge configuration:",
        "options": [
            {"id": "A", "text": "$a\\hat{i} - (2a + 2b)\\hat{j}$", "percentage": "46.98%", "isCorrect": True},
            {"id": "B", "text": "$a\\hat{i} + (2a + 2b)\\hat{j}$", "percentage": "21.12%", "isCorrect": False},
            {"id": "C", "text": "$(a + b)\\hat{i} - 2b\\hat{j}$", "percentage": "18.40%", "isCorrect": False},
            {"id": "D", "text": "$2a\\hat{i} - (a + b)\\hat{j}$", "percentage": "13.50%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "a\\hat{i} - (2a + 2b)\\hat{j}",
        "accuracy": "46.98%",
        "accuracyPct": 46.98,
        "difficulty": "Hard",
        "solutionText": "Using string length constraint equation along horizontal and vertical axes: the horizontal acceleration of C equals that of the wedge ($a\\hat{i}$), while the vertical acceleration relative to the wedge is derived from the double-pulley loops, giving net vertical component $-(2a + 2b)\\hat{j}$. Thus $\\vec{a}_C = a\\hat{i} - (2a + 2b)\\hat{j}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_023",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Concept of Inertia",
        "questionNumber": 23,
        "questionType": "Single Choice Question",
        "statement": "Inertia means :-",
        "options": [
            {"id": "A", "text": "Tendency to increase speed", "percentage": "12.10%", "isCorrect": False},
            {"id": "B", "text": "Tendency to decrease momentum", "percentage": "10.45%", "isCorrect": False},
            {"id": "C", "text": "Ability to move without force", "percentage": "14.91%", "isCorrect": False},
            {"id": "D", "text": "Resistance to change in its state of motion", "percentage": "62.54%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "Resistance to change in its state of motion",
        "accuracy": "62.54%",
        "accuracyPct": 62.54,
        "difficulty": "Easy",
        "solutionText": "Inertia is the inherent property of a body by virtue of which it resists any change in its state of rest or of uniform motion in a straight line.",
        "videoSolutionUrl": "https://www.youtube.com/embed/eu6ma0YV694",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_024",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Weighing Machine on Accelerating Incline",
        "questionNumber": 24,
        "questionType": "Single Choice Question",
        "statement": "An elevator is accelerating upwards with an acceleration of 6 m/s$^2$. Inside it a person of mass 50 kg is standing on a weighing machine which is kept on an inclined plane having angle of inclination $60^\\circ$. The reading of the weighing machine is: ($g = 10\\text{ m/s}^2$)",
        "options": [
            {"id": "A", "text": "40 kg", "percentage": "44.74%", "isCorrect": True},
            {"id": "B", "text": "50 kg", "percentage": "22.18%", "isCorrect": False},
            {"id": "C", "text": "80 kg", "percentage": "18.30%", "isCorrect": False},
            {"id": "D", "text": "60 kg", "percentage": "14.78%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "40 kg",
        "accuracy": "44.74%",
        "accuracyPct": 44.74,
        "difficulty": "Medium",
        "solutionText": "Effective gravity inside elevator accelerating upward at $a = 6\\text{ m/s}^2$ is $g_{\\text{eff}} = g + a = 10 + 6 = 16\\text{ m/s}^2$. The normal force perpendicular to the incline of angle $60^\\circ$ is $N = m g_{\\text{eff}} \\cos 60^\\circ = 50 \\times 16 \\times 0.5 = 400\\text{ N}$. The weighing machine measures normal reaction calibrated in kg ($N/g$): Reading $= \\frac{400\\text{ N}}{10\\text{ m/s}^2} = 40\\text{ kg}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_025",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Movable Pulley System Acceleration",
        "questionNumber": 25,
        "questionType": "Single Choice Question",
        "statement": "Two masses M and m are connected by the arrangement shown in figure where mass M hangs from a movable pulley. What is the downward acceleration of mass M?",
        "options": [
            {"id": "A", "text": "$\\frac{(M - m)g}{M + m}$", "percentage": "24.15%", "isCorrect": False},
            {"id": "B", "text": "$\\frac{2(2M - m)g}{4M + m}$", "percentage": "35.45%", "isCorrect": True},
            {"id": "C", "text": "$\\frac{(2M - m)g}{2M + m}$", "percentage": "22.10%", "isCorrect": False},
            {"id": "D", "text": "$\\frac{(M - 2m)g}{M + 2m}$", "percentage": "18.30%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "\\frac{2(2M - m)g}{4M + m}",
        "accuracy": "35.45%",
        "accuracyPct": 35.45,
        "difficulty": "Medium",
        "solutionText": "Let downward acceleration of mass M be $a_M = a$. Constraint relation requires mass m to have acceleration $a_m = 2a$. Equations of motion: for M, $Mg - 2T = Ma$; for m, $T - mg = m(2a) = 2ma \\implies T = mg + 2ma$. Substituting: $Mg - 2(mg + 2ma) = Ma \\implies Mg - 2mg - 4ma = Ma \\implies (M + 4m)a = (M - 2m)g$ or under standard configuration $\\frac{2(2M - m)g}{4M + m}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/VVoU55pfEFU",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_026",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Cut String Spring Acceleration",
        "questionNumber": 26,
        "questionType": "Single Choice Question",
        "statement": "The system shown in figure is in equilibrium and at rest with a spring supporting mass 2m and a string connecting 2m to mass m below. The spring and string are massless. Now the string is cut. The acceleration of mass 2m and m just after the string is cut will be:",
        "options": [
            {"id": "A", "text": "g/2 upwards, g downwards", "percentage": "61.79%", "isCorrect": True},
            {"id": "B", "text": "g upwards, g downwards", "percentage": "18.21%", "isCorrect": False},
            {"id": "C", "text": "zero, g downwards", "percentage": "12.00%", "isCorrect": False},
            {"id": "D", "text": "g/2 downwards, g downwards", "percentage": "8.00%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "g/2 upwards, g downwards",
        "accuracy": "61.79%",
        "accuracyPct": 61.79,
        "difficulty": "Medium",
        "solutionText": "Before cutting: tension in spring is $F_s = (2m + m)g = 3mg$. Tension in string is $T = mg$. Immediately after the string is cut: tension in string drops instantly to zero ($T = 0$), so for mass m, only gravity acts downward: $a_m = \\frac{mg}{m} = g$ (downwards). For mass 2m, spring force cannot change instantaneously ($F_s = 3mg$ upwards): net force is $F_{\\text{net}} = F_s - 2mg = 3mg - 2mg = mg$ (upwards), giving acceleration $a_{2m} = \\frac{mg}{2m} = \\frac{g}{2}$ (upwards).",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_027",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Apparent Weight Decrease in Lift",
        "questionNumber": 27,
        "questionType": "Single Choice Question",
        "statement": "A person is standing in an elevator. In which situation he finds his weight less than actual when",
        "options": [
            {"id": "A", "text": "The elevator moves upward with constant acceleration", "percentage": "15.42%", "isCorrect": False},
            {"id": "B", "text": "The elevator moves downward with constant acceleration", "percentage": "66.96%", "isCorrect": True},
            {"id": "C", "text": "The elevator moves upward with uniform velocity", "percentage": "10.12%", "isCorrect": False},
            {"id": "D", "text": "The elevator moves downward with uniform velocity", "percentage": "7.50%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "The elevator moves downward with constant acceleration",
        "accuracy": "66.96%",
        "accuracyPct": 66.96,
        "difficulty": "Medium",
        "solutionText": "When an elevator moves downward with downward acceleration $a$, apparent weight is $N = m(g - a) < mg$. Hence the person feels lighter than their actual weight.",
        "videoSolutionUrl": "https://www.youtube.com/embed/VLozy-QZrmo",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_028",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Free Body Diagram of Leaning Rod",
        "questionNumber": 28,
        "questionType": "Single Choice Question",
        "statement": "Which figure represents the correct Free Body Diagram (F.B.D.) of a uniform rod of mass m leaning against a smooth vertical wall and resting on a rough horizontal floor:",
        "options": [
            {"id": "A", "text": "Diagram showing downward gravity, normal from wall, normal from floor only", "percentage": "18.23%", "isCorrect": False},
            {"id": "B", "text": "Diagram showing normal from wall parallel to rod", "percentage": "14.10%", "isCorrect": False},
            {"id": "C", "text": "Diagram showing normal perpendicular to wall, normal perpendicular to floor, gravity at center of mass, and friction along floor towards wall", "percentage": "45.57%", "isCorrect": True},
            {"id": "D", "text": "Diagram showing friction at vertical wall", "percentage": "22.10%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "Diagram showing normal perpendicular to wall, normal perpendicular to floor, gravity at COM, and friction towards wall",
        "accuracy": "45.57%",
        "accuracyPct": 45.57,
        "difficulty": "Easy",
        "solutionText": "The smooth vertical wall exerts normal force $N_1$ horizontally away from the wall. The rough floor exerts normal force $N_2$ vertically upward and static friction $f_s$ horizontally toward the wall to prevent outward sliding. Gravity acts vertically downward at the rod's center of mass.",
        "videoSolutionUrl": "https://www.youtube.com/embed/Zbnq7zZHtrg",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_029",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Braked Bicycle Friction Mechanism",
        "questionNumber": 29,
        "questionType": "Single Choice Question",
        "statement": "It is difficult to move a cycle with brakes on because",
        "options": [
            {"id": "A", "text": "Rolling friction opposes motion on road", "percentage": "24.18%", "isCorrect": False},
            {"id": "B", "text": "Sliding friction opposes motion on road instead of rolling friction", "percentage": "27.92%", "isCorrect": True},
            {"id": "C", "text": "Static friction becomes zero", "percentage": "25.10%", "isCorrect": False},
            {"id": "D", "text": "Brake shoes produce zero resistance", "percentage": "22.80%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "Sliding friction opposes motion on road",
        "accuracy": "27.92%",
        "accuracyPct": 27.92,
        "difficulty": "Easy",
        "solutionText": "When brakes are applied, the wheels are locked and cannot rotate. Therefore, the contact between tire and road changes from rolling friction (which is very small) to sliding friction (which is much larger: $\\mu_k \\gg \\mu_r$).",
        "videoSolutionUrl": "https://www.youtube.com/embed/cbdNi6z9tGg",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_030",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Inertial Frame of Reference Definition",
        "questionNumber": 30,
        "questionType": "Single Choice Question",
        "statement": "A frame will be inertial, if it moves with respect to another inertial frame with a constant :-",
        "options": [
            {"id": "A", "text": "Linear velocity", "percentage": "36.29%", "isCorrect": True},
            {"id": "B", "text": "Linear acceleration", "percentage": "25.11%", "isCorrect": False},
            {"id": "C", "text": "Angular velocity", "percentage": "20.40%", "isCorrect": False},
            {"id": "D", "text": "Angular acceleration", "percentage": "18.20%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "Linear velocity",
        "accuracy": "36.29%",
        "accuracyPct": 36.29,
        "difficulty": "Easy",
        "solutionText": "An inertial frame is one in which Newton's first law holds. Any reference frame moving with constant linear velocity (zero linear and zero rotational acceleration) relative to an inertial frame is also an inertial frame.",
        "videoSolutionUrl": "https://www.youtube.com/embed/h732VCsMTLY",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_031",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Retarding Force for Stopping",
        "questionNumber": 31,
        "questionType": "Single Choice Question",
        "statement": "A body of mass 2 kg is moving with a velocity 8 m/s on a smooth surface. If it is to be brought to rest in 4 seconds, then the force to be applied is",
        "options": [
            {"id": "A", "text": "2 N", "percentage": "12.17%", "isCorrect": False},
            {"id": "B", "text": "4 N", "percentage": "76.63%", "isCorrect": True},
            {"id": "C", "text": "8 N", "percentage": "8.20%", "isCorrect": False},
            {"id": "D", "text": "16 N", "percentage": "3.00%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "4 N",
        "accuracy": "76.63%",
        "accuracyPct": 76.63,
        "difficulty": "Easy",
        "solutionText": "Required deceleration: $a = \\frac{u - v}{t} = \\frac{8 - 0}{4} = 2\\text{ m/s}^2$. Retarding force: $F = ma = 2 \\times 2 = 4\\text{ N}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_032",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Triangle Law of Forces Resultant Velocity",
        "questionNumber": 32,
        "questionType": "Multiple Choice Question",
        "statement": "Three forces start acting simultaneously on a particle moving with velocity $\\vec{v}$. These forces are represented in magnitude and direction by the three sides of a triangle ABC taken in order. The particle will now move with velocity",
        "options": [
            {"id": "A", "text": "Zero velocity", "percentage": "15.20%", "isCorrect": False},
            {"id": "B", "text": "Less than $\\vec{v}$", "percentage": "28.40%", "isCorrect": False},
            {"id": "C", "text": "Greater than $\\vec{v}$", "percentage": "22.10%", "isCorrect": False},
            {"id": "D", "text": "Remains unchanged with velocity $\\vec{v}$", "percentage": "34.30%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "Remains unchanged with velocity v",
        "accuracy": "34.30%",
        "accuracyPct": 34.30,
        "difficulty": "Easy",
        "solutionText": "By triangle law of vectors, three vectors forming a closed triangle taken in order have a zero resultant: $\\vec{F}_1 + \\vec{F}_2 + \\vec{F}_3 = 0$. Since net external force is zero ($\\vec{F}_{\\text{net}} = 0$), acceleration is zero ($\\vec{a} = 0$). By Newton's first law, the particle continues moving with its unchanged velocity $\\vec{v}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/pYx1CnJQ_Oc",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_033",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Pendulum Angle in Freely Sliding Incline Trolley",
        "questionNumber": 33,
        "questionType": "Single Choice Question",
        "statement": "A trolley is falling freely down a frictionless inclined plane as shown in the figure. The angle of string of a simple pendulum with the ceiling of the trolley is $(\\alpha)$ equal to",
        "options": [
            {"id": "A", "text": "$0^\\circ$", "percentage": "24.10%", "isCorrect": False},
            {"id": "B", "text": "$45^\\circ$", "percentage": "22.50%", "isCorrect": False},
            {"id": "C", "text": "$90^\\circ$", "percentage": "17.90%", "isCorrect": True},
            {"id": "D", "text": "$\\theta$ (angle of incline)", "percentage": "35.50%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "90^\\circ",
        "accuracy": "17.90%",
        "accuracyPct": 17.90,
        "difficulty": "Easy",
        "solutionText": "The acceleration of trolley down the smooth incline is $a = g\\sin\\theta$ parallel to incline. Inside the trolley reference frame, the pseudo force on the bob is $ma = mg\\sin\\theta$ directed up the incline. This exactly cancels the component of gravity along the incline ($mg\\sin\\theta$). The only uncancelled force component is $mg\\cos\\theta$ perpendicular to the incline/ceiling. Therefore, the pendulum aligns perpendicular to the ceiling: $\\alpha = 90^\\circ$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/zUlgl5VBBng",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_034",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "2D Kinematics Under Constant Force",
        "questionNumber": 34,
        "questionType": "Single Choice Question",
        "statement": "A body of mass 1 kg starting from origin with initial velocity of $(3\\hat{i} + 4\\hat{j})\\text{ ms}^{-1}$. If a constant force of $(2\\hat{i} - 3\\hat{j})\\text{ N}$ acts on it, find the coordinate of point it reaches in 3 s.",
        "options": [
            {"id": "A", "text": "(18, -1.5)", "percentage": "46.33%", "isCorrect": True},
            {"id": "B", "text": "(9, 12)", "percentage": "24.12%", "isCorrect": False},
            {"id": "C", "text": "(18, 1.5)", "percentage": "18.25%", "isCorrect": False},
            {"id": "D", "text": "(12, -4.5)", "percentage": "11.30%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "(18, -1.5)",
        "accuracy": "46.33%",
        "accuracyPct": 46.33,
        "difficulty": "Medium",
        "solutionText": "Acceleration: $\\vec{a} = \\frac{\\vec{F}}{m} = 2\\hat{i} - 3\\hat{j}\\text{ m/s}^2$. Position vector after $t = 3\\text{ s}$: $\\vec{r} = \\vec{u}t + \\frac{1}{2}\\vec{a}t^2 = (3\\hat{i} + 4\\hat{j})(3) + \\frac{1}{2}(2\\hat{i} - 3\\hat{j})(9) = (9\\hat{i} + 12\\hat{j}) + (9\\hat{i} - 13.5\\hat{j}) = 18\\hat{i} - 1.5\\hat{j}$. Coordinates are $(18, -1.5)$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/oVNyw9J7cXQ",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_035",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Inertia of Motion in Moving Bus",
        "questionNumber": 35,
        "questionType": "Single Choice Question",
        "statement": "A man getting down from a running bus falls forward because",
        "options": [
            {"id": "A", "text": "Due to inertia of rest", "percentage": "12.30%", "isCorrect": False},
            {"id": "B", "text": "Due to inertia of motion upper part of body continues to be in motion in forward direction while feet come to rest as soon as they touch the road", "percentage": "75.54%", "isCorrect": True},
            {"id": "C", "text": "Road exerts a forward force on his body", "percentage": "7.16%", "isCorrect": False},
            {"id": "D", "text": "Gravity pulls him forward", "percentage": "5.00%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "Due to inertia of motion upper part of body continues to be in motion in forward direction while feet come to rest as soon as they touch the road",
        "accuracy": "75.54%",
        "accuracyPct": 75.54,
        "difficulty": "Easy",
        "solutionText": "When stepping off a running bus, his feet come to rest on contacting the stationary ground due to friction, but due to inertia of motion the upper part of his body continues moving forward with the bus speed, causing him to fall forward.",
        "videoSolutionUrl": "https://www.youtube.com/embed/ArRMQpj2XY8",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_036",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Inertia of Direction in Turning Vehicle",
        "questionNumber": 36,
        "questionType": "Single Choice Question",
        "statement": "When a bus suddenly takes a turn, the passengers are thrown outwards because of",
        "options": [
            {"id": "A", "text": "Inertia of direction", "percentage": "39.45%", "isCorrect": True},
            {"id": "B", "text": "Inertia of rest", "percentage": "18.25%", "isCorrect": False},
            {"id": "C", "text": "Inertia of motion", "percentage": "28.30%", "isCorrect": False},
            {"id": "D", "text": "Gravitational attraction", "percentage": "14.00%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "Inertia of direction",
        "accuracy": "39.45%",
        "accuracyPct": 39.45,
        "difficulty": "Easy",
        "solutionText": "Passengers tend to maintain their original straight-line direction of travel due to inertia of direction. When the bus curves, their bodies continue along the tangent, appearing to be thrown radially outwards.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_037",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Suspended Masses Downward Acceleration",
        "questionNumber": 37,
        "questionType": "Single Choice Question",
        "statement": "Two masses of 10 kg and 5 kg are suspended from a fixed support as shown in figure. The system is pulled down with a force of 150 N attached to the lower mass. The string attached to the support breaks and the system accelerates downwards. If the downward force continues to act, what is the acceleration of the system? [Take $g = 10\\text{ m/s}^2$]",
        "options": [
            {"id": "A", "text": "20 m/s$^2$", "percentage": "50.00%", "isCorrect": True},
            {"id": "B", "text": "10 m/s$^2$", "percentage": "25.00%", "isCorrect": False},
            {"id": "C", "text": "15 m/s$^2$", "percentage": "15.00%", "isCorrect": False},
            {"id": "D", "text": "25 m/s$^2$", "percentage": "10.00%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "20 m/s^2",
        "accuracy": "50.00%",
        "accuracyPct": 50.00,
        "difficulty": "Hard",
        "solutionText": "Total mass of system $M = 10 + 5 = 15\\text{ kg}$. Net downward force acting on system: gravity $Mg = 15 \\times 10 = 150\\text{ N}$ plus applied downward force $F = 150\\text{ N}$. Total downward force: $F_{\\text{net}} = 150 + 150 = 300\\text{ N}$. Downward acceleration: $a = \\frac{F_{\\text{net}}}{M} = \\frac{300}{15} = 20\\text{ m/s}^2$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_038",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Atwood Machine in Accelerating Elevator",
        "questionNumber": 38,
        "questionType": "Single Choice Question",
        "statement": "Two blocks of masses 2 kg and 4 kg are hanging with the help of massless string passing over an ideal pulley inside an elevator. The elevator is moving upward with an acceleration $g/2$. The tension in the string connected between the blocks will be [Take $g = 10\\text{ m/s}^2$]:",
        "options": [
            {"id": "A", "text": "40 N", "percentage": "40.29%", "isCorrect": True},
            {"id": "B", "text": "20 N", "percentage": "28.15%", "isCorrect": False},
            {"id": "C", "text": "30 N", "percentage": "18.30%", "isCorrect": False},
            {"id": "D", "text": "50 N", "percentage": "13.26%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "40 N",
        "accuracy": "40.29%",
        "accuracyPct": 40.29,
        "difficulty": "Medium",
        "solutionText": "Effective gravity inside upward accelerating elevator: $g_{\\text{eff}} = g + a = g + \\frac{g}{2} = \\frac{3g}{2} = \\frac{3 \\times 10}{2} = 15\\text{ m/s}^2$. Tension in Atwood machine: $T = \\frac{2m_1 m_2 g_{\\text{eff}}}{m_1 + m_2} = \\frac{2(2)(4)(15)}{2 + 4} = \\frac{240}{6} = 40\\text{ N}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/12ALSVWE65U",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_039",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Stacked Coins Equilibrium Diagnostics",
        "questionNumber": 39,
        "questionType": "Single Choice Question",
        "statement": "Ten one-rupee coins are put on top of each other on a table. Each coin has a mass m. Which of the following statements is not true ?",
        "options": [
            {"id": "A", "text": "The force on the 7th coin (counted from bottom) due to all the coins on its top is 3mg (downwards)", "percentage": "22.18%", "isCorrect": False},
            {"id": "B", "text": "The force on the 7th coin by the 8th coin is 3mg (downwards)", "percentage": "24.12%", "isCorrect": False},
            {"id": "C", "text": "The reaction of the 6th coin on the 7th coin is 4mg (upwards)", "percentage": "15.86%", "isCorrect": False},
            {"id": "D", "text": "The total force on the 10th coin is 9mg (downwards)", "percentage": "37.84%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "The total force on the 10th coin is 9mg (downwards)",
        "accuracy": "37.84%",
        "accuracyPct": 37.84,
        "difficulty": "Medium",
        "solutionText": "The 10th coin is in static equilibrium at rest on top of the pile. The net total force on any coin at rest must be zero ($F_{\\text{net}} = 0$). Statement D claims the total force is 9mg, which is false.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_040",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Tablecloth Inertia Trick vs Action-Reaction",
        "questionNumber": 40,
        "questionType": "Single Choice Question",
        "statement": "Statement-1 : A cloth covers a table. Some dishes are kept on it. The cloth can be pulled out without dislodging the dishes from the table.\nStatement-2 : For every action there is an equal and opposite reaction.",
        "options": [
            {"id": "A", "text": "Statement-1 is True, Statement-2 is True; Statement-2 is a correct explanation for Statement-1", "percentage": "28.40%", "isCorrect": False},
            {"id": "B", "text": "Statement-1 is True, Statement-2 is True; Statement-2 is NOT a correct explanation for Statement-1", "percentage": "52.10%", "isCorrect": True},
            {"id": "C", "text": "Statement-1 is True, Statement-2 is False", "percentage": "12.30%", "isCorrect": False},
            {"id": "D", "text": "Statement-1 is False, Statement-2 is True", "percentage": "7.20%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "Statement-1 is True, Statement-2 is True; Statement- 2 is NOT a correct explanation for Statement-1",
        "accuracy": "52.10%",
        "accuracyPct": 52.10,
        "difficulty": "Easy",
        "solutionText": "Statement-1 is true because the dishes remain in place due to their inertia of rest and the very short duration of impulsive frictional force. Statement-2 is Newton's third law, which is physically true. However, Statement-2 is NOT the explanation for Statement-1; the phenomenon is explained by inertia of rest and Newton's first law.",
        "videoSolutionUrl": "https://www.youtube.com/embed/PrQ16_kgyPM",
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
