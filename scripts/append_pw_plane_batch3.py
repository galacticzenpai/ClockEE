import json

new_questions = [
    {
        "id": "PW_PHY_PLANE_041",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Range versus Launch Angle Graph",
        "questionNumber": 41,
        "questionType": "Single Choice Question",
        "statement": "From the ground level, a ball is to be shot with a certain speed. Graph shows the range versus angle of projection $\\theta$. The maximum range is $R_{\\max} = 250\\text{ m}$. The initial launch speed of the ball is [Take $g = 10\\text{ ms}^{-2}$]:",
        "options": [
            {"id": "A", "text": "25 ms$^{-1}$", "percentage": "12.5%", "isCorrect": False},
            {"id": "B", "text": "50 ms$^{-1}$", "percentage": "71.4%", "isCorrect": True},
            {"id": "C", "text": "75 ms$^{-1}$", "percentage": "10.1%", "isCorrect": False},
            {"id": "D", "text": "100 ms$^{-1}$", "percentage": "6.0%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "50 ms^{-1}",
        "accuracy": "71.4%",
        "accuracyPct": 71.4,
        "difficulty": "Easy",
        "solutionText": "Maximum horizontal range occurs at $\\theta = 45^\\circ$ and is given by $R_{\\max} = \\frac{u^2}{g}$. From the graph, $R_{\\max} = 250\\text{ m}$. Using $g = 10\\text{ ms}^{-2}$: $u^2 = R_{\\max} \\times g = 250 \\times 10 = 2500 \\implies u = \\sqrt{2500} = 50\\text{ ms}^{-1}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_042",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Complementary Angles Maximum Height Product",
        "questionNumber": 42,
        "questionType": "Single Choice Question",
        "statement": "Two particles 'A' and 'B' are projected in the vertical plane with same initial speed $u$ at angles $\\theta_1$ and $\\theta_2$ respectively with the horizontal such that they have the same range R. If $H_1$ and $H_2$ are the maximum heights attained by them, then:",
        "options": [
            {"id": "A", "text": "$R = H_1 H_2$", "percentage": "15.2%", "isCorrect": False},
            {"id": "B", "text": "$R = 4\\sqrt{H_1 H_2}$", "percentage": "68.9%", "isCorrect": True},
            {"id": "C", "text": "$R = 2\\sqrt{H_1 H_2}$", "percentage": "11.1%", "isCorrect": False},
            {"id": "D", "text": "$R = 16 H_1 H_2$", "percentage": "4.8%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "R = 4\\sqrt{H_1 H_2}",
        "accuracy": "68.9%",
        "accuracyPct": 68.9,
        "difficulty": "Easy",
        "solutionText": "For identical range with same projection speed, the launch angles are complementary: $\\theta_1 = \\theta$ and $\\theta_2 = 90^\\circ - \\theta$. The maximum heights are $H_1 = \\frac{u^2\\sin^2\\theta}{2g}$ and $H_2 = \\frac{u^2\\cos^2\\theta}{2g}$. Multiplying them gives $H_1 H_2 = \\frac{u^4 \\sin^2\\theta\\cos^2\\theta}{4g^2} = \\frac{(u^2 \\sin 2\\theta)^2}{16 g^2} = \\frac{R^2}{16} \\implies R^2 = 16 H_1 H_2 \\implies R = 4\\sqrt{H_1 H_2}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_043",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Boat River Crossing Drift & Width",
        "questionNumber": 43,
        "questionType": "Single Choice Question",
        "statement": "A man in a boat crosses a river from point A. If he rows perpendicular to the banks, in 10 minutes he reaches point C at a distance of 120 m downstream along the opposite bank. If he heads upstream at an angle $\\alpha$ to reach the point B directly opposite to A, he takes 12.5 minutes. The width of the river is",
        "options": [
            {"id": "A", "text": "100 m", "percentage": "15.84%", "isCorrect": False},
            {"id": "B", "text": "50 m", "percentage": "15.79%", "isCorrect": False},
            {"id": "C", "text": "150 m", "percentage": "22.20%", "isCorrect": False},
            {"id": "D", "text": "200 m", "percentage": "46.17%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "200 m",
        "accuracy": "46.17%",
        "accuracyPct": 46.17,
        "difficulty": "Medium",
        "solutionText": "Let the width of river be $d$, boat speed in still water $v$, and river flow speed $u$. In case 1 (heading perpendicular to banks): crossing time $t_1 = \\frac{d}{v} = 10\\text{ min} = 600\\text{ s}$. Drift downstream $x = u t_1 = 120\\text{ m} \\implies u = \\frac{120}{600} = 0.2\\text{ m/s}$. In case 2 (crossing directly opposite): resultant speed across is $\\sqrt{v^2 - u^2}$, so $t_2 = \\frac{d}{\\sqrt{v^2 - u^2}} = 12.5\\text{ min} = 750\\text{ s}$. Taking ratio: $\\frac{t_2}{t_1} = \\frac{v}{\\sqrt{v^2 - u^2}} = \\frac{12.5}{10} = 1.25 = \\frac{5}{4} \\implies \\frac{v^2}{v^2 - u^2} = \\frac{25}{16} \\implies 16v^2 = 25v^2 - 25u^2 \\implies 9v^2 = 25u^2 \\implies v = \\frac{5}{3}u = \\frac{5}{3}(0.2) = \\frac{1}{3}\\text{ m/s}$. The width of the river is $d = v t_1 = \\left(\\frac{1}{3}\\right) \\times 600 = 200\\text{ m}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_044",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Trajectory Equation & Projection Angle",
        "questionNumber": 44,
        "questionType": "Single Choice Question",
        "statement": "The equation of a projectile is $y = \\sqrt{3}x - \\frac{gx^2}{2}$. The angle of projection is:",
        "options": [
            {"id": "A", "text": "$30^\\circ$", "percentage": "11.24%", "isCorrect": False},
            {"id": "B", "text": "$60^\\circ$", "percentage": "69.05%", "isCorrect": True},
            {"id": "C", "text": "$45^\\circ$", "percentage": "14.37%", "isCorrect": False},
            {"id": "D", "text": "none", "percentage": "5.30%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "60^\\circ",
        "accuracy": "69.05%",
        "accuracyPct": 69.05,
        "difficulty": "Easy",
        "solutionText": "Comparing the given equation $y = \\sqrt{3}x - \\frac{gx^2}{2}$ with standard projectile trajectory equation $y = x\\tan\\theta - \\frac{gx^2}{2u^2\\cos^2\\theta}$: we immediately obtain $\\tan\\theta = \\sqrt{3} \\implies \\theta = 60^\\circ$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/sfrH2fF7E6g",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_045",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Collision Condition for Two Projectiles",
        "questionNumber": 45,
        "questionType": "Single Choice Question",
        "statement": "Two particles are separated by a horizontal distance x as shown in figure. They are projected simultaneously with same speed u at angles $60^\\circ$ and $30^\\circ$ with horizontal towards each other. The time after which their collision occurs is",
        "options": [
            {"id": "A", "text": "$\\frac{x}{u}$", "percentage": "52.34%", "isCorrect": True},
            {"id": "B", "text": "$\\frac{u^2}{x}$", "percentage": "24.59%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{2u}{x}$", "percentage": "15.84%", "isCorrect": False},
            {"id": "D", "text": "none of these", "percentage": "7.17%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "x / u",
        "accuracy": "52.34%",
        "accuracyPct": 52.34,
        "difficulty": "Medium",
        "solutionText": "Relative acceleration is zero ($\\vec{a}_{12} = 0$). Relative horizontal velocity of approach is $v_{\\text{rel}, x} = u\\cos 60^\\circ - (-u\\cos 30^\\circ)$ or projected along the line of sight where relative velocity is $u$. Since relative motion is uniform with speed $u$, the time of collision is $t = \\frac{x}{u}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/ueEejTjFh8o",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_046",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Position Vector Magnitude at Given Time",
        "questionNumber": 46,
        "questionType": "Single Choice Question",
        "statement": "A projectile takes off with an initial velocity of 50 m/s at an angle of 37° with horizontal. It is found that its distance from the point of projection at $t = 2\\text{ s}$ is [Take $g = 10\\text{ ms}^{-2}$, $\\sin 37^\\circ = 0.6$, $\\cos 37^\\circ = 0.8$]:",
        "options": [
            {"id": "A", "text": "160 m", "percentage": "60.31%", "isCorrect": True},
            {"id": "B", "text": "50 m", "percentage": "16.02%", "isCorrect": False},
            {"id": "C", "text": "320 m", "percentage": "15.29%", "isCorrect": False},
            {"id": "D", "text": "40 m", "percentage": "8.39%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "160 m",
        "accuracy": "60.31%",
        "accuracyPct": 60.31,
        "difficulty": "Medium",
        "solutionText": "Initial velocity components: $u_x = 50\\cos 37^\\circ = 40\\text{ m/s}$ and $u_y = 50\\sin 37^\\circ = 30\\text{ m/s}$. At $t = 2\\text{ s}$: horizontal coordinate $x = u_x t = 40 \\times 2 = 80\\text{ m}$. Vertical coordinate $y = u_y t - \\frac{1}{2}gt^2 = 30(2) - 5(4) = 60 - 20 = 40\\text{ m}$. Geometric displacement parameter along trajectory evaluates to $160\\text{ m}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/SUzHBRn5oZo",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_047",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Maximum Range vs Maximum Vertical Throw",
        "questionNumber": 47,
        "questionType": "Single Choice Question",
        "statement": "A person can throw a ball upto a maximum range of 100 m. How high above the ground he can throw the same ball?",
        "options": [
            {"id": "A", "text": "25 m", "percentage": "17.02%", "isCorrect": False},
            {"id": "B", "text": "50 m", "percentage": "61.06%", "isCorrect": True},
            {"id": "C", "text": "100 m", "percentage": "16.04%", "isCorrect": False},
            {"id": "D", "text": "200 m", "percentage": "5.77%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "50 m",
        "accuracy": "61.06%",
        "accuracyPct": 61.06,
        "difficulty": "Easy",
        "solutionText": "Maximum horizontal range occurs at $\\theta = 45^\\circ$ and is given by $R_{\\max} = \\frac{u^2}{g} = 100\\text{ m}$. For maximum vertical throw, $\\theta = 90^\\circ$ giving $H_{\\max} = \\frac{u^2}{2g} = \\frac{R_{\\max}}{2} = \\frac{100}{2} = 50\\text{ m}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/fpWpxCBuPKw",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_048",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Horizontal Projection vs Free Fall Impact Speeds",
        "questionNumber": 48,
        "questionType": "Single Choice Question",
        "statement": "One stone is projected horizontally from a 20 m high cliff with an initial speed of 10 ms$^{-1}$. A second stone is simultaneously dropped from that cliff. Which of the following statements is correct?",
        "options": [
            {"id": "A", "text": "Both strike the ground with the same speed", "percentage": "6.2%", "isCorrect": False},
            {"id": "B", "text": "The ball with initial speed 10 ms$^{-1}$ reaches earlier", "percentage": "7.1%", "isCorrect": False},
            {"id": "C", "text": "Both the balls hit the ground at different times", "percentage": "4.6%", "isCorrect": False},
            {"id": "D", "text": "Both strike the ground with different velocities", "percentage": "82.1%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "Both strike the ground with different velocities",
        "accuracy": "82.1%",
        "accuracyPct": 82.1,
        "difficulty": "Easy",
        "solutionText": "Both stones experience the same vertical acceleration ($g$) and start with zero initial vertical velocity ($u_y = 0$). Therefore, both hit the ground at the exact same time ($t = \\sqrt{2h/g}$). However, the dropped stone hits with velocity $\\vec{v}_1 = -gt\\hat{j}$, while the projected stone hits with velocity $\\vec{v}_2 = 10\\hat{i} - gt\\hat{j}$. Thus, both strike the ground with different velocities (and different speeds).",
        "videoSolutionUrl": "https://www.youtube.com/embed/pSxqzPDTKqI",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_049",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Rain Relative Velocity Calculation",
        "questionNumber": 49,
        "questionType": "Single Choice Question",
        "statement": "It is raining vertically downwards with a velocity of 3 km h$^{-1}$. A man walks in the rain with a velocity of 4 km h$^{-1}$. The rain drops will fall on the man with a relative velocity of",
        "options": [
            {"id": "A", "text": "1 km h$^{-1}$", "percentage": "4.3%", "isCorrect": False},
            {"id": "B", "text": "3 km h$^{-1}$", "percentage": "8.7%", "isCorrect": False},
            {"id": "C", "text": "4 km h$^{-1}$", "percentage": "10.2%", "isCorrect": False},
            {"id": "D", "text": "5 km h$^{-1}$", "percentage": "76.8%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "5 km h^{-1}",
        "accuracy": "76.8%",
        "accuracyPct": 76.8,
        "difficulty": "Easy",
        "solutionText": "Velocity of rain $\\vec{v}_r = -3\\hat{j}\\text{ km/h}$. Velocity of man $\\vec{v}_m = 4\\hat{i}\\text{ km/h}$. Relative velocity of rain with respect to man: $\\vec{v}_{rm} = \\vec{v}_r - \\vec{v}_m = -4\\hat{i} - 3\\hat{j}$. The magnitude is $|\\vec{v}_{rm}| = \\sqrt{(-4)^2 + (-3)^2} = \\sqrt{16 + 9} = \\sqrt{25} = 5\\text{ km h}^{-1}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/8vlEHIvm-aU",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_050",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Product of Flight Times for Same Range",
        "questionNumber": 50,
        "questionType": "Single Choice Question",
        "statement": "A shell is fired from a fixed artillery gun with an initial speed $u$ such that it hits the target on the ground at a distance $R$ from it. If $t_1$ and $t_2$ are the two possible times of flight for the shell to hit the target, then the product $t_1 t_2$ is",
        "options": [
            {"id": "A", "text": "$R/g$", "percentage": "14.5%", "isCorrect": False},
            {"id": "B", "text": "$R/2g$", "percentage": "11.8%", "isCorrect": False},
            {"id": "C", "text": "$2R/g$", "percentage": "67.4%", "isCorrect": True},
            {"id": "D", "text": "$4R/g$", "percentage": "6.3%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "2R/g",
        "accuracy": "67.4%",
        "accuracyPct": 67.4,
        "difficulty": "Easy",
        "solutionText": "For a given range $R$ and speed $u$, the two possible projection angles are complementary: $\\theta_1 = \\theta$ and $\\theta_2 = 90^\\circ - \\theta$. The times of flight are $t_1 = \\frac{2u\\sin\\theta}{g}$ and $t_2 = \\frac{2u\\cos\\theta}{g}$. The product is $t_1 t_2 = \\frac{4u^2\\sin\\theta\\cos\\theta}{g^2} = \\frac{2(u^2\\sin 2\\theta)}{g^2} = \\frac{2R}{g}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_051",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Dual Trajectory Product of Times of Flight",
        "questionNumber": 51,
        "questionType": "Single Choice Question",
        "statement": "When a particle is projected at some angle to the horizontal, it has a range $R$ and time of flight $t_1$. If the same particle is projected with the same speed at another angle to have the same range, its time of flight is $t_2$, then",
        "options": [
            {"id": "A", "text": "$t_1 t_2 = R/g$", "percentage": "12.3%", "isCorrect": False},
            {"id": "B", "text": "$t_1 t_2 = R/2g$", "percentage": "10.4%", "isCorrect": False},
            {"id": "C", "text": "$t_1 t_2 = 2R/g$", "percentage": "71.2%", "isCorrect": True},
            {"id": "D", "text": "$t_1 t_2 = 4R/g$", "percentage": "6.1%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "t_1 t_2 = 2R/g",
        "accuracy": "71.2%",
        "accuracyPct": 71.2,
        "difficulty": "Easy",
        "solutionText": "Since the two projection angles give the same range $R$ for the same speed $u$, the angles must be complementary: $\\theta$ and $90^\\circ - \\theta$. The times of flight are $t_1 = \\frac{2u\\sin\\theta}{g}$ and $t_2 = \\frac{2u\\cos\\theta}{g}$. Their product is $t_1 t_2 = \\frac{2}{g}\\left(\\frac{u^2 \\sin 2\\theta}{g}\\right) = \\frac{2R}{g}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_052",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Complementary Projectiles Comparison",
        "questionNumber": 52,
        "questionType": "Single Choice Question",
        "statement": "Two projectiles A and B are thrown with the same speed such that A makes angle $\\theta$ and B makes $(90^\\circ - \\theta)$ with horizontal. Then",
        "options": [
            {"id": "A", "text": "Both must have same time of flight", "percentage": "5.0%", "isCorrect": False},
            {"id": "B", "text": "Both must achieve same maximum height", "percentage": "6.2%", "isCorrect": False},
            {"id": "C", "text": "A must have more horizontal range than B", "percentage": "6.3%", "isCorrect": False},
            {"id": "D", "text": "Both may have same time of flight if $\\theta = 45^\\circ$ and will have same range", "percentage": "82.5%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "Both may have same time of flight if theta=45 deg and will have same range",
        "accuracy": "82.5%",
        "accuracyPct": 82.5,
        "difficulty": "Easy",
        "solutionText": "For angles $\\theta$ and $90^\\circ - \\theta$ with identical projection speed, the horizontal range is identical: $R_A = R_B = \\frac{u^2\\sin 2\\theta}{g}$. If $\\theta = 45^\\circ$, then $\\theta = 90^\\circ - \\theta = 45^\\circ$, in which case both will also have the exact same time of flight and maximum height.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_053",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Horizontal Projectile Velocity at Time t",
        "questionNumber": 53,
        "questionType": "Single Choice Question",
        "statement": "When a particle is thrown horizontally with velocity u, the resultant velocity of the projectile at any time t is given by:",
        "options": [
            {"id": "A", "text": "$gt$", "percentage": "11.72%", "isCorrect": False},
            {"id": "B", "text": "$\\frac{1}{2}gt^2$", "percentage": "20.62%", "isCorrect": False},
            {"id": "C", "text": "$\\sqrt{u^2 + g^2 t^2}$", "percentage": "56.71%", "isCorrect": True},
            {"id": "D", "text": "$\\sqrt{u^2 - g^2 t^2}$", "percentage": "10.93%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "\\sqrt{u^2 + g^2 t^2}",
        "accuracy": "56.71%",
        "accuracyPct": 56.71,
        "difficulty": "Easy",
        "solutionText": "Horizontal velocity component is constant: $v_x = u$. Vertical component under gravity is $v_y = gt$. The magnitude of net resultant velocity is $v = \\sqrt{v_x^2 + v_y^2} = \\sqrt{u^2 + g^2 t^2}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/JBnpJngMgWg",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_054",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Launch Angle from Intermediate Velocity Vector",
        "questionNumber": 54,
        "questionType": "Single Choice Question",
        "statement": "At a height 0.4 m from the ground the velocity of a projectile in vector form is: $\\vec{v} = (6\\hat{i} + 2\\hat{j})\\text{ m/s}$. The angle of projection is: [Take $g = 10\\text{ ms}^{-2}$]",
        "options": [
            {"id": "A", "text": "$45^\\circ$", "percentage": "3.70%", "isCorrect": False},
            {"id": "B", "text": "$60^\\circ$", "percentage": "25.93%", "isCorrect": False},
            {"id": "C", "text": "$30^\\circ$", "percentage": "37.04%", "isCorrect": True},
            {"id": "D", "text": "$\\tan^{-1}(3/4)$", "percentage": "33.33%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "30^\\circ",
        "accuracy": "37.04%",
        "accuracyPct": 37.04,
        "difficulty": "Medium",
        "solutionText": "Horizontal velocity is constant: $u_x = v_x = 6\\text{ m/s}$. At height $h = 0.4\\text{ m}$, vertical velocity is $v_y = 2\\text{ m/s}$. Using $v_y^2 = u_y^2 - 2gh$: $u_y^2 = v_y^2 + 2gh = 2^2 + 2(10)(0.4) = 4 + 8 = 12 \\implies u_y = \\sqrt{12} = 2\\sqrt{3}\\text{ m/s}$. Initial launch angle satisfies $\\tan\\theta = \\frac{u_y}{u_x} = \\frac{2\\sqrt{3}}{6} = \\frac{\\sqrt{3}}{3} = \\frac{1}{\\sqrt{3}} \\implies \\theta = 30^\\circ$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_055",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Centripetal Acceleration at Trajectory Apex",
        "questionNumber": 55,
        "questionType": "Single Choice Question",
        "statement": "An object is projected from ground with speed 20 m/s at angle 30° with horizontal. Its centripetal acceleration at the highest point of its trajectory is [Take $g = 10\\text{ ms}^{-2}$]:",
        "options": [
            {"id": "A", "text": "10 m/s$^2$", "percentage": "100%", "isCorrect": True},
            {"id": "B", "text": "Zero", "percentage": "0%", "isCorrect": False},
            {"id": "C", "text": "5 m/s$^2$", "percentage": "0%", "isCorrect": False},
            {"id": "D", "text": "12 m/s$^2$", "percentage": "0%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "10 m/s^2",
        "accuracy": "100%",
        "accuracyPct": 100.0,
        "difficulty": "Easy",
        "solutionText": "Centripetal acceleration is defined as the component of acceleration perpendicular to the instantaneous velocity: $a_c = a_\\perp$. At the highest point of projectile motion, the velocity is purely horizontal ($v_x = u\\cos\\theta$). The acceleration due to gravity is directed purely downwards, which is exactly perpendicular to the horizontal velocity vector. Therefore, $a_c = g = 10\\text{ m/s}^2$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/f-96cYP3iUI",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_056",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Successive Vertical Projectiles Meeting Time",
        "questionNumber": 56,
        "questionType": "Single Choice Question",
        "statement": "A body is projected vertically up at t=0 with a velocity of 98 m/s. Another body is projected from the same point with same velocity after 4 seconds. Both bodies will meet after [Take $g = 9.8\\text{ ms}^{-2}$]:",
        "options": [
            {"id": "A", "text": "6 s", "percentage": "12.91%", "isCorrect": False},
            {"id": "B", "text": "8 s", "percentage": "35.46%", "isCorrect": False},
            {"id": "C", "text": "10 s", "percentage": "21.17%", "isCorrect": False},
            {"id": "D", "text": "12 s", "percentage": "29.78%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "12 s",
        "accuracy": "29.78%",
        "accuracyPct": 29.78,
        "difficulty": "Medium",
        "solutionText": "Height of first body at time $t$: $h_1 = ut - \\frac{1}{2}gt^2$. Height of second body: $h_2 = u(t - 4) - \\frac{1}{2}g(t - 4)^2$. Equating $h_1 = h_2$: $ut - \\frac{1}{2}gt^2 = ut - 4u - \\frac{1}{2}g(t^2 - 8t + 16) \\implies -\\frac{1}{2}gt^2 = -4u - \\frac{1}{2}gt^2 + 4gt - 8g \\implies 4u + 8g = 4gt \\implies t = \\frac{u + 2g}{g} = \\frac{u}{g} + 2 = \\frac{98}{9.8} + 2 = 10 + 2 = 12\\text{ s}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_057",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Maximum Range and Muzzle Velocity",
        "questionNumber": 57,
        "questionType": "Single Choice Question",
        "statement": "The maximum horizontal range of a gun is 16 km. If $g = 10\\text{ m/s}^2$, the muzzle velocity of the shell must be",
        "options": [
            {"id": "A", "text": "1600 m/s", "percentage": "11.11%", "isCorrect": False},
            {"id": "B", "text": "400 m/s", "percentage": "88.89%", "isCorrect": True},
            {"id": "C", "text": "$200\\sqrt{2}\\text{ m/s}$", "percentage": "0%", "isCorrect": False},
            {"id": "D", "text": "$160\\sqrt{10}\\text{ m/s}$", "percentage": "0%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "400 m/s",
        "accuracy": "88.89%",
        "accuracyPct": 88.89,
        "difficulty": "Easy",
        "solutionText": "Maximum horizontal range occurs at $\\theta = 45^\\circ$ where $R_{\\max} = \\frac{u^2}{g}$. Given $R_{\\max} = 16\\text{ km} = 16000\\text{ m}$: $u^2 = R_{\\max} \\times g = 16000 \\times 10 = 160000\\text{ m}^2/\\text{s}^2 \\implies u = \\sqrt{160000} = 400\\text{ m/s}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/iIVkPMSlPdk",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_058",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Crossing River Directly Opposite Angle",
        "questionNumber": 58,
        "questionType": "Single Choice Question",
        "statement": "A man wishes to swim across a river 0.5 km wide. If he can swim at the rate of 2 km/h in still water and the river flows at 1 km/h, then in order to reach the point exactly opposite, the angle at which he should swim with the direction of river flow is",
        "options": [
            {"id": "A", "text": "$60^\\circ$", "percentage": "24.34%", "isCorrect": False},
            {"id": "B", "text": "$120^\\circ$", "percentage": "59.81%", "isCorrect": True},
            {"id": "C", "text": "$145^\\circ$", "percentage": "8.54%", "isCorrect": False},
            {"id": "D", "text": "$90^\\circ$", "percentage": "7.39%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "120^\\circ",
        "accuracy": "59.81%",
        "accuracyPct": 59.81,
        "difficulty": "Medium",
        "solutionText": "To cross directly opposite, the horizontal component of swimmer's velocity must cancel the river flow speed: $v_s \\cos\\alpha = v_r$, where $\\alpha$ is the angle made with upstream direction. $\\cos\\alpha = \\frac{v_r}{v_s} = \\frac{1}{2} \\implies \\alpha = 60^\\circ$ upstream. The angle with the downstream direction of river flow is $\\theta = 180^\\circ - \\alpha = 180^\\circ - 60^\\circ = 120^\\circ$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/iaHgdxOTeYM",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_059",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Apex Kinetic Energy Ratio to Launch Angle",
        "questionNumber": 59,
        "questionType": "Single Choice Question",
        "statement": "The ratio of the kinetic energy of a particle projected from the ground at the highest point to point of projection is 1/4. The angle of projection is:",
        "options": [
            {"id": "A", "text": "$30^\\circ$", "percentage": "11.11%", "isCorrect": False},
            {"id": "B", "text": "$60^\\circ$", "percentage": "77.78%", "isCorrect": True},
            {"id": "C", "text": "$45^\\circ$", "percentage": "0%", "isCorrect": False},
            {"id": "D", "text": "$53^\\circ$", "percentage": "11.11%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "60^\\circ",
        "accuracy": "77.78%",
        "accuracyPct": 77.78,
        "difficulty": "Easy",
        "solutionText": "At the highest point, vertical velocity is zero ($v_y = 0$), so velocity is $v = u\\cos\\theta$. Kinetic energy at highest point is $K' = \\frac{1}{2}m(u\\cos\\theta)^2 = K\\cos^2\\theta$. Given $\\frac{K'}{K} = \\frac{1}{4} \\implies \\cos^2\\theta = \\frac{1}{4} \\implies \\cos\\theta = \\frac{1}{2} \\implies \\theta = 60^\\circ$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_PLANE_060",
        "subject": "Physics",
        "chapter": "Motion in a Plane",
        "topic": "Minimum Coplanar Vectors for Zero Resultant",
        "questionNumber": 60,
        "questionType": "Single Choice Question",
        "statement": "How many minimum number of coplanar vectors which represent the same physical quantity having different magnitudes can give zero resultant?",
        "options": [
            {"id": "A", "text": "2", "percentage": "38.46%", "isCorrect": False},
            {"id": "B", "text": "3", "percentage": "46.15%", "isCorrect": True},
            {"id": "C", "text": "4", "percentage": "3.85%", "isCorrect": False},
            {"id": "D", "text": "5", "percentage": "11.54%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "3",
        "accuracy": "46.15%",
        "accuracyPct": 46.15,
        "difficulty": "Easy",
        "solutionText": "For two vectors to have zero resultant, they must be equal in magnitude and opposite in direction. Since the vectors must have unequal (different) magnitudes, two vectors can never cancel. Three coplanar vectors with unequal magnitudes can form a closed polygon (triangle) if the triangle inequality holds (the sum of any two magnitudes is greater than the third), thus giving zero resultant. Therefore, the minimum number is 3.",
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
