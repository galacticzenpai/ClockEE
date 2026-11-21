import json

new_questions = [
    {
        "id": "PW_PHY_NLM_001",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Newton's Second Law & Constant Force",
        "questionNumber": 1,
        "questionType": "Single Choice Question",
        "statement": "A constant force acting on a body of mass 3.0 kg changes its speed from 2.0 m s$^{-1}$ to 3.5 m s$^{-1}$ in 25 s. The direction of the motion of the body remains unchanged. What is the magnitude and direction of the force?",
        "options": [
            {"id": "A", "text": "0.18 N, in the direction of motion", "percentage": "87.03%", "isCorrect": True},
            {"id": "B", "text": "0.36 N, in the direction of motion", "percentage": "6.12%", "isCorrect": False},
            {"id": "C", "text": "0.18 N, opposite to the direction of motion", "percentage": "4.25%", "isCorrect": False},
            {"id": "D", "text": "0.36 N, opposite to the direction of motion", "percentage": "2.60%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "0.18 N, in the direction of motion",
        "accuracy": "87.03%",
        "accuracyPct": 87.03,
        "difficulty": "Easy",
        "solutionText": "Acceleration is $a = \\frac{v - u}{t} = \\frac{3.5 - 2.0}{25} = \\frac{1.5}{25} = 0.06\\text{ m s}^{-2}$. Force magnitude is $F = ma = 3.0 \\times 0.06 = 0.18\\text{ N}$. Since speed increases without changing direction, force acts in the direction of motion.",
        "videoSolutionUrl": "https://www.youtube.com/embed/yAwhUuaP2mg",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_002",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Net Force & Motion with Resistance",
        "questionNumber": 2,
        "questionType": "Single Choice Question",
        "statement": "A car of mass 1000 kg is moving with a velocity of 10 m/s and is acted upon by a forward force of 1000 N due to engine and retarding force of 500 N due to friction. Its velocity after 10 seconds is",
        "options": [
            {"id": "A", "text": "10 m/s", "percentage": "12.15%", "isCorrect": False},
            {"id": "B", "text": "15 m/s", "percentage": "66.83%", "isCorrect": True},
            {"id": "C", "text": "20 m/s", "percentage": "15.42%", "isCorrect": False},
            {"id": "D", "text": "25 m/s", "percentage": "5.60%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "15 m/s",
        "accuracy": "66.83%",
        "accuracyPct": 66.83,
        "difficulty": "Easy",
        "solutionText": "Net forward force: $F_{\\text{net}} = F_{\\text{engine}} - f = 1000 - 500 = 500\\text{ N}$. Acceleration: $a = \\frac{F_{\\text{net}}}{m} = \\frac{500}{1000} = 0.5\\text{ m/s}^2$. Velocity after 10 s: $v = u + at = 10 + (0.5)(10) = 10 + 5 = 15\\text{ m/s}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/Qj7wVn2tYw0",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_003",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Spring Balance Reading & Upward Acceleration",
        "questionNumber": 3,
        "questionType": "Single Choice Question",
        "statement": "A spring toy weighing 1 kg on a spring balance suddenly jumps upward. A boy standing near the toy notices that the scale of the balance reads 1.05 kg. In this process the maximum acceleration of the toy is ($g = 10\\text{ m/s}^2$)",
        "options": [
            {"id": "A", "text": "0.05 m/s$^2$", "percentage": "22.31%", "isCorrect": False},
            {"id": "B", "text": "0.5 m/s$^2$", "percentage": "56.49%", "isCorrect": True},
            {"id": "C", "text": "5 m/s$^2$", "percentage": "14.20%", "isCorrect": False},
            {"id": "D", "text": "0.25 m/s$^2$", "percentage": "7.00%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "0.5 m/s^2",
        "accuracy": "56.49%",
        "accuracyPct": 56.49,
        "difficulty": "Easy",
        "solutionText": "Apparent weight recorded by balance: $N = m(g + a) = 1.05g$. Since true mass $m = 1\\text{ kg}$, $1(g + a) = 1.05g \\implies a = 0.05g = 0.05 \\times 10 = 0.5\\text{ m/s}^2$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_004",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Newton's Laws Conceptual Matching",
        "questionNumber": 4,
        "questionType": "Single Choice Question",
        "statement": "Match Column I with Column II:\nColumn I: (A) Law of inertia, (B) $F = \\frac{dp}{dt}$, (C) Action and reaction, (D) Apparent weight inside accelerating lift\nColumn II: (p) First law of motion, (q) Second law of motion, (r) Third law of motion, (s) Fictive or pseudo force",
        "options": [
            {"id": "A", "text": "A-p, B-q, C-r, D-s", "percentage": "95.03%", "isCorrect": True},
            {"id": "B", "text": "A-q, B-p, C-r, D-s", "percentage": "2.10%", "isCorrect": False},
            {"id": "C", "text": "A-p, B-r, C-q, D-s", "percentage": "1.87%", "isCorrect": False},
            {"id": "D", "text": "A-s, B-q, C-r, D-p", "percentage": "1.00%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "A-p, B-q, C-r, D-s",
        "accuracy": "95.03%",
        "accuracyPct": 95.03,
        "difficulty": "Easy",
        "solutionText": "Law of inertia is Newton's 1st law (A-p). $F = dp/dt$ is Newton's 2nd law (B-q). Action-reaction is Newton's 3rd law (C-r). Apparent weight in non-inertial accelerating lift is explained using pseudo/fictive force (D-s).",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_005",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Connected Blocks on Rough Incline",
        "questionNumber": 5,
        "questionType": "Single Choice Question",
        "statement": "Two blocks A and B of masses m and 2m respectively are held at rest on a rough inclined plane of inclination $45^\\circ$. The coefficient of friction between block A and plane is $2\\mu$ and that between block B and plane is $\\mu$. When the blocks are released, the acceleration of the combination is",
        "options": [
            {"id": "A", "text": "$g(1 - \\mu)/\\sqrt{2}$", "percentage": "16.12%", "isCorrect": False},
            {"id": "B", "text": "$g(1 + \\mu)/3$", "percentage": "10.25%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{g}{\\sqrt{2}}\\left(1 - \\frac{4\\mu}{3}\\right)$", "percentage": "66.53%", "isCorrect": True},
            {"id": "D", "text": "$g(1 - 2\\mu)/3$", "percentage": "7.10%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "\\frac{g}{\\sqrt{2}}(1 - \\frac{4\\mu}{3})",
        "accuracy": "66.53%",
        "accuracyPct": 66.53,
        "difficulty": "Medium",
        "solutionText": "Total driving force down the incline: $F_{\\text{down}} = (m + 2m)g\\sin 45^\\circ = 3mg\\sin 45^\\circ$. Total friction force: $f_A + f_B = (2\\mu)(mg\\cos 45^\\circ) + (\\mu)(2mg\\cos 45^\\circ) = 4\\mu mg\\cos 45^\\circ$. Acceleration $a = \\frac{3mg\\sin 45^\\circ - 4\\mu mg\\cos 45^\\circ}{3m} = \\frac{g}{\\sqrt{2}}\\left(1 - \\frac{4\\mu}{3}\\right)$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_006",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Friction vs Applied Force Graph",
        "questionNumber": 6,
        "questionType": "Single Choice Question",
        "statement": "A body of mass 2 kg is placed on a rough horizontal surface. A horizontal force F is applied on it. The variation of frictional force f with applied force F is as shown in figure. The limiting friction is 8 N. The coefficient of static friction is ($g = 10\\text{ m/s}^2$):",
        "options": [
            {"id": "A", "text": "0.2", "percentage": "18.21%", "isCorrect": False},
            {"id": "B", "text": "0.4", "percentage": "53.64%", "isCorrect": True},
            {"id": "C", "text": "0.5", "percentage": "21.15%", "isCorrect": False},
            {"id": "D", "text": "0.8", "percentage": "7.00%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "0.4",
        "accuracy": "53.64%",
        "accuracyPct": 53.64,
        "difficulty": "Medium",
        "solutionText": "Normal reaction $N = mg = 2 \\times 10 = 20\\text{ N}$. Limiting static friction $f_L = 8\\text{ N}$. Using $f_L = \\mu_s N \\implies \\mu_s = \\frac{f_L}{N} = \\frac{8}{20} = 0.4$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_007",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Contact Force Variation with Incline Angle",
        "questionNumber": 7,
        "questionType": "Single Choice Question",
        "statement": "A block of mass m is placed on a rough inclined plane of inclination $\\theta$. As the angle $\\theta$ is increased from $0^\\circ$ to $90^\\circ$, the contact force between the block and the incline",
        "options": [
            {"id": "A", "text": "remains constant throughout", "percentage": "12.30%", "isCorrect": False},
            {"id": "B", "text": "first increases and then decreases", "percentage": "24.12%", "isCorrect": False},
            {"id": "C", "text": "first remains constant and then decreases", "percentage": "49.63%", "isCorrect": True},
            {"id": "D", "text": "decreases continuously", "percentage": "13.95%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "first remains constant and then decreases",
        "accuracy": "49.63%",
        "accuracyPct": 49.63,
        "difficulty": "Hard",
        "solutionText": "For $\\theta \\le \\theta_r$ (angle of repose), the block remains at rest. Normal force $N = mg\\cos\\theta$ and static friction $f = mg\\sin\\theta$. Total contact force is $R = \\sqrt{N^2 + f^2} = \\sqrt{(mg\\cos\\theta)^2 + (mg\\sin\\theta)^2} = mg = \\text{constant}$. For $\\theta > \\theta_r$, the block slides, so kinetic friction is $f_k = \\mu_k mg\\cos\\theta$. Contact force is $R = \\sqrt{N^2 + f_k^2} = mg\\cos\\theta\\sqrt{1 + \\mu_k^2}$, which decreases monotonically as $\\theta \\to 90^\\circ$. Hence $R$ first remains constant ($mg$) and then decreases.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_008",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Atwood Machine String Tension",
        "questionNumber": 8,
        "questionType": "Single Choice Question",
        "statement": "Two masses $m_1$ and $m_2$ ($m_1 > m_2$) are connected by a light inextensible string passing over a frictionless pulley. When the system is released from rest, the tension in the string is",
        "options": [
            {"id": "A", "text": "$\\frac{2m_1 m_2 g}{m_1 + m_2}$", "percentage": "78.50%", "isCorrect": True},
            {"id": "B", "text": "$\\frac{m_1 m_2 g}{m_1 + m_2}$", "percentage": "11.20%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{(m_1 - m_2)g}{m_1 + m_2}$", "percentage": "6.10%", "isCorrect": False},
            {"id": "D", "text": "$\\frac{(m_1 + m_2)g}{2m_1 m_2}$", "percentage": "4.20%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "\\frac{2m_1 m_2 g}{m_1 + m_2}",
        "accuracy": "78.50%",
        "accuracyPct": 78.50,
        "difficulty": "Easy",
        "solutionText": "Equations of motion: $m_1 g - T = m_1 a$ and $T - m_2 g = m_2 a$. Acceleration $a = \\frac{(m_1 - m_2)g}{m_1 + m_2}$. Substituting into tension expression: $T = m_2(g + a) = m_2\\left(g + \\frac{(m_1 - m_2)g}{m_1 + m_2}\\right) = \\frac{2m_1 m_2 g}{m_1 + m_2}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_009",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Contact Force Between Blocks",
        "questionNumber": 9,
        "questionType": "Single Choice Question",
        "statement": "Three blocks of masses 2 kg, 3 kg and 5 kg are placed in contact on a smooth horizontal surface as shown in figure. A horizontal force of 10 N is applied on the 2 kg block. The contact force between the 3 kg and 5 kg block is",
        "options": [
            {"id": "A", "text": "5 N", "percentage": "68.39%", "isCorrect": True},
            {"id": "B", "text": "8 N", "percentage": "15.41%", "isCorrect": False},
            {"id": "C", "text": "2 N", "percentage": "10.20%", "isCorrect": False},
            {"id": "D", "text": "3 N", "percentage": "6.00%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "5 N",
        "accuracy": "68.39%",
        "accuracyPct": 68.39,
        "difficulty": "Easy",
        "solutionText": "Total mass $M = 2 + 3 + 5 = 10\\text{ kg}$. System acceleration $a = \\frac{F}{M} = \\frac{10}{10} = 1\\text{ m/s}^2$. The contact force between 3 kg and 5 kg accelerates the 5 kg block: $N_{35} = m_3 a = 5 \\times 1 = 5\\text{ N}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_010",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Climbing Monkey Rope Tension",
        "questionNumber": 10,
        "questionType": "Single Choice Question",
        "statement": "A monkey of mass 20 kg is climbing on a vertical rope with an acceleration of 2 m/s$^2$ in upward direction. If the breaking strength of the rope is 300 N, then the rope will ($g = 10\\text{ m/s}^2$)",
        "options": [
            {"id": "A", "text": "break", "percentage": "24.12%", "isCorrect": False},
            {"id": "B", "text": "not break", "percentage": "63.83%", "isCorrect": True},
            {"id": "C", "text": "break only after 10 seconds", "percentage": "7.50%", "isCorrect": False},
            {"id": "D", "text": "cannot be determined", "percentage": "4.55%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "not break",
        "accuracy": "63.83%",
        "accuracyPct": 63.83,
        "difficulty": "Easy",
        "solutionText": "When climbing upwards with acceleration $a$, tension in rope is $T = m(g + a) = 20(10 + 2) = 20 \\times 12 = 240\\text{ N}$. Since $240\\text{ N} < 300\\text{ N}$ (breaking strength), the rope will not break.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_011",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Static Friction and Actual Friction Force",
        "questionNumber": 11,
        "questionType": "Single Choice Question",
        "statement": "A block of mass 5 kg is lying on a rough horizontal surface. The coefficient of static friction between block and surface is 0.4. A horizontal force of 15 N is applied on the block. The frictional force acting on the block is ($g = 10\\text{ m/s}^2$)",
        "options": [
            {"id": "A", "text": "15 N", "percentage": "68.51%", "isCorrect": True},
            {"id": "B", "text": "20 N", "percentage": "22.34%", "isCorrect": False},
            {"id": "C", "text": "10 N", "percentage": "6.15%", "isCorrect": False},
            {"id": "D", "text": "0 N", "percentage": "3.00%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "15 N",
        "accuracy": "68.51%",
        "accuracyPct": 68.51,
        "difficulty": "Easy",
        "solutionText": "Limiting static friction: $f_L = \\mu_s mg = 0.4 \\times 5 \\times 10 = 20\\text{ N}$. Since applied force $F = 15\\text{ N} < f_L = 20\\text{ N}$, the block remains at rest. Friction is static and self-adjusting, exactly balancing applied force: $f = F = 15\\text{ N}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_012",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Coefficient of Kinetic Friction",
        "questionNumber": 12,
        "questionType": "Single Choice Question",
        "statement": "A block of mass 10 kg is placed on a rough horizontal plane. When a horizontal force of 20 N is applied on it, it moves with constant velocity. The coefficient of kinetic friction is ($g = 10\\text{ m/s}^2$)",
        "options": [
            {"id": "A", "text": "0.1", "percentage": "12.40%", "isCorrect": False},
            {"id": "B", "text": "0.2", "percentage": "77.29%", "isCorrect": True},
            {"id": "C", "text": "0.3", "percentage": "6.11%", "isCorrect": False},
            {"id": "D", "text": "0.4", "percentage": "4.20%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "0.2",
        "accuracy": "77.29%",
        "accuracyPct": 77.29,
        "difficulty": "Easy",
        "solutionText": "Moving with constant velocity implies zero net acceleration ($a = 0$). Hence applied force balances kinetic friction: $F = f_k = \\mu_k mg \\implies \\mu_k = \\frac{F}{mg} = \\frac{20}{10 \\times 10} = \\frac{20}{100} = 0.2$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_013",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Normal Force Reduction & Sliding Inception",
        "questionNumber": 13,
        "questionType": "Single Choice Question",
        "statement": "In the figure shown, horizontal force F1 is applied on a block but the block does not slide. Then as the magnitude of vertical upward force F2 is increased from zero the block begins to slide. The correct statement is",
        "options": [
            {"id": "A", "text": "Coefficient of friction decreases", "percentage": "18.12%", "isCorrect": False},
            {"id": "B", "text": "Normal force increases", "percentage": "14.20%", "isCorrect": False},
            {"id": "C", "text": "Maximum value of static frictional force decreases", "percentage": "50.78%", "isCorrect": True},
            {"id": "D", "text": "Horizontal force F1 increases automatically", "percentage": "16.90%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "Maximum value of static frictional force decreases",
        "accuracy": "50.78%",
        "accuracyPct": 50.78,
        "difficulty": "Medium",
        "solutionText": "Upward vertical force $F_2$ reduces normal force: $N = mg - F_2$. Limiting static friction is $f_{\\max} = \\mu_s N = \\mu_s(mg - F_2)$. As $F_2$ increases, $N$ decreases, so $f_{\\max}$ decreases. When $f_{\\max} < F_1$, the block begins to slide.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_014",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Block on Accelerating Trolley",
        "questionNumber": 14,
        "questionType": "Single Choice Question",
        "statement": "A block of mass 15 kg is placed on a long trolley. The coefficient of friction between the block and trolley is 0.18. The trolley accelerates from rest with 0.5 m/s$^2$ for 20 s. Then what is the friction force acting on the block? [Take $g = 10\\text{ m/s}^2$]",
        "options": [
            {"id": "A", "text": "27 N", "percentage": "22.15%", "isCorrect": False},
            {"id": "B", "text": "15 N", "percentage": "14.25%", "isCorrect": False},
            {"id": "C", "text": "7.5 N", "percentage": "55.90%", "isCorrect": True},
            {"id": "D", "text": "3.75 N", "percentage": "7.70%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "7.5 N",
        "accuracy": "55.90%",
        "accuracyPct": 55.90,
        "difficulty": "Medium",
        "solutionText": "Maximum static friction: $f_L = \\mu mg = 0.18 \\times 15 \\times 10 = 27\\text{ N}$. Force required to accelerate the block with trolley ($a = 0.5\\text{ m/s}^2$): $F_{\\text{req}} = ma = 15 \\times 0.5 = 7.5\\text{ N}$. Since $F_{\\text{req}} = 7.5\\text{ N} < f_L = 27\\text{ N}$, the block does not slip relative to trolley. Friction force acting is $f = 7.5\\text{ N}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/IuLgm91pwhk",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_015",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Apparent Weight in Accelerating Lift",
        "questionNumber": 15,
        "questionType": "Single Choice Question",
        "statement": "A man of mass 60 kg is riding in a lift. The weights of the man, when the lift is accelerating upwards and downwards at 2 m/s$^2$ are respectively ($g = 10\\text{ m/s}^2$):",
        "options": [
            {"id": "A", "text": "720 N and 480 N", "percentage": "69.70%", "isCorrect": True},
            {"id": "B", "text": "480 N and 720 N", "percentage": "16.10%", "isCorrect": False},
            {"id": "C", "text": "600 N and 600 N", "percentage": "8.20%", "isCorrect": False},
            {"id": "D", "text": "720 N and 600 N", "percentage": "6.00%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "720 N and 480 N",
        "accuracy": "69.70%",
        "accuracyPct": 69.70,
        "difficulty": "Medium",
        "solutionText": "Upward acceleration: $W_1 = m(g + a) = 60(10 + 2) = 60 \\times 12 = 720\\text{ N}$. Downward acceleration: $W_2 = m(g - a) = 60(10 - 2) = 60 \\times 8 = 480\\text{ N}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_016",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Impulse-Momentum Theorem & Contact Time",
        "questionNumber": 16,
        "questionType": "Single Choice Question",
        "statement": "A ball of mass 50 g is dropped from a height of 20 m. A boy on the ground hits the ball vertically upwards with a bat with an average force of 200 N, so that it attains a vertical height of 45 m. The time for which the ball remains in contact with the bat is [Take $g = 10\\text{ m/s}^2$]",
        "options": [
            {"id": "A", "text": "1/20th of a second", "percentage": "22.15%", "isCorrect": False},
            {"id": "B", "text": "1/40th of a second", "percentage": "25.38%", "isCorrect": False},
            {"id": "C", "text": "1/80th of a second", "percentage": "33.47%", "isCorrect": True},
            {"id": "D", "text": "1/100th of a second", "percentage": "19.00%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "1/80th of a second",
        "accuracy": "33.47%",
        "accuracyPct": 33.47,
        "difficulty": "Easy",
        "solutionText": "Speed on arrival: $v_1 = \\sqrt{2gh_1} = \\sqrt{2 \\times 10 \\times 20} = 20\\text{ m/s}$ (downwards). Speed on departure: $v_2 = \\sqrt{2gh_2} = \\sqrt{2 \\times 10 \\times 45} = 30\\text{ m/s}$ (upwards). Change in momentum: $\\Delta p = m(v_2 - (-v_1)) = 0.05(30 + 20) = 0.05 \\times 50 = 2.5\\text{ N s}$. Contact time: $\\Delta t = \\frac{\\Delta p}{F} = \\frac{2.5}{200} = \\frac{1}{80}\\text{ s}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_017",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Pulley Constraint Relations",
        "questionNumber": 17,
        "questionType": "Multiple Choice Question",
        "statement": "In the pulley-block system shown in figure, strings and pulleys are light and ideal. Select the correct alternative(s):",
        "options": [
            {"id": "A", "text": "Acceleration of block A is related to block B by constraint equation", "percentage": "46.85%", "isCorrect": True},
            {"id": "B", "text": "Tension in string connecting block B is half the tension supporting block A", "percentage": "29.30%", "isCorrect": True},
            {"id": "C", "text": "Mechanical advantage of movable pulley is 2", "percentage": "31.91%", "isCorrect": True},
            {"id": "D", "text": "Displacement of A is half that of B", "percentage": "22.92%", "isCorrect": True}
        ],
        "correctOption": "A, B, C, D",
        "correctAnswer": "All options correct",
        "accuracy": "24.00%",
        "accuracyPct": 24.00,
        "difficulty": "Easy",
        "solutionText": "For standard movable pulley supporting block A with free end attached to block B: length constraint $2x_A + x_B = L \\implies 2a_A + a_B = 0$. Hence $a_B = 2a_A$, $x_B = 2x_A$, tension on block A is $2T$, and mechanical advantage is 2. All statements A, B, C, and D are valid.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_018",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Inertia & Uniform Straight Motion",
        "questionNumber": 18,
        "questionType": "Single Choice Question",
        "statement": "A particle is moving with a constant speed along a straight line path. A force is not required to:",
        "options": [
            {"id": "A", "text": "increase its speed", "percentage": "10.25%", "isCorrect": False},
            {"id": "B", "text": "decrease its momentum", "percentage": "9.80%", "isCorrect": False},
            {"id": "C", "text": "change the direction of motion", "percentage": "9.20%", "isCorrect": False},
            {"id": "D", "text": "keep it moving with uniform velocity", "percentage": "70.75%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "keep it moving with uniform velocity",
        "accuracy": "70.75%",
        "accuracyPct": 70.75,
        "difficulty": "Easy",
        "solutionText": "According to Newton's first law of motion (law of inertia), an object continues in its state of rest or uniform motion in a straight line unless acted upon by a net external force. Thus, zero net force is required to maintain uniform velocity.",
        "videoSolutionUrl": "https://www.youtube.com/embed/YLB6RNq8wuU",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_019",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Conservation of Momentum & Newton's Laws",
        "questionNumber": 19,
        "questionType": "Single Choice Question",
        "statement": "Choose the correct statement(s) from the following:\nI. Recoiling of a gun is an application of principle of conservation of linear momentum.\nII. Explosion of a bomb in mid-air conserves total linear momentum because net external force is zero.",
        "options": [
            {"id": "A", "text": "Only I", "percentage": "28.40%", "isCorrect": False},
            {"id": "B", "text": "Only II", "percentage": "16.50%", "isCorrect": False},
            {"id": "C", "text": "Both I and II", "percentage": "45.10%", "isCorrect": True},
            {"id": "D", "text": "Neither I nor II", "percentage": "10.00%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "Both I and II",
        "accuracy": "45.10%",
        "accuracyPct": 45.10,
        "difficulty": "Easy",
        "solutionText": "Both statements are correct physical applications of linear momentum conservation under zero net external impulsive force.",
        "videoSolutionUrl": "https://www.youtube.com/embed/lqJK64ykK9A",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_020",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Self-Adjusting Friction Force",
        "questionNumber": 20,
        "questionType": "Single Choice Question",
        "statement": "Which of the following is a self-adjusting force?",
        "options": [
            {"id": "A", "text": "Static friction", "percentage": "65.91%", "isCorrect": True},
            {"id": "B", "text": "Kinetic friction", "percentage": "16.19%", "isCorrect": False},
            {"id": "C", "text": "Limiting friction", "percentage": "12.40%", "isCorrect": False},
            {"id": "D", "text": "Rolling friction", "percentage": "5.50%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "Static friction",
        "accuracy": "65.91%",
        "accuracyPct": 65.91,
        "difficulty": "Easy",
        "solutionText": "Static friction adjusts its magnitude and direction to match the applied horizontal force until the limiting friction threshold is reached ($0 \\le f_s \\le f_L$). Hence static friction is a self-adjusting force.",
        "videoSolutionUrl": "https://www.youtube.com/embed/yAwhUuaP2mg",
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
