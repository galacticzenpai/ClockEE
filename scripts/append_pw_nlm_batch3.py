import json

new_questions = [
    {
        "id": "PW_PHY_NLM_041",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Inertia of Motion",
        "questionNumber": 41,
        "questionType": "Single Choice Question",
        "statement": "A man getting down a running bus, falls forward because:",
        "options": [
            {"id": "A", "text": "due to inertia of rest, road is left behind and man reaches forward", "percentage": "4.53%", "isCorrect": False},
            {"id": "B", "text": "due to inertia of motion upper part of body continues to be in motion in forward direction while feet come to rest as soon as they touch the road", "percentage": "83.95%", "isCorrect": True},
            {"id": "C", "text": "he leans forward as a matter of habit", "percentage": "2.06%", "isCorrect": False},
            {"id": "D", "text": "of the combined effect of all the three factors stated in (1), (2) and (3)", "percentage": "10.29%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "due to inertia of motion upper part of body continues to be in motion in forward direction while feet come to rest as soon as they touch the road",
        "accuracy": "83.95%",
        "accuracyPct": 83.95,
        "difficulty": "Medium",
        "solutionText": "When a passenger steps out of a moving bus, his feet come to rest immediately upon touching the ground due to friction, but due to inertia of motion, the upper part of his body continues moving forward in the direction of the bus, causing him to fall forward.",
        "videoSolutionUrl": "https://www.youtube.com/embed/oyEFwND8ecc",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_042",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Spring Force Dynamics & Sudden Release",
        "questionNumber": 42,
        "questionType": "Single Choice Question",
        "statement": "A block tied between two identical springs is in equilibrium. If upper spring is cut then the acceleration of the block just after cut is 6 m/s$^2$ downwards. Now, if instead of upper spring, lower spring is being cut then the acceleration of the block just after the cut will be: (take $g = 10\\text{ m/s}^2$)",
        "diagramUrl": "https://d2bps9p1kiy4ka.cloudfront.net/5b09189f7285894d9130ccd0/f1ff7aae-4e98-479e-bd17-132b474d1eb7.png",
        "options": [
            {"id": "A", "text": "$4\\text{ m/s}^2$ downwards", "percentage": "27.47%", "isCorrect": True},
            {"id": "B", "text": "$6\\text{ m/s}^2$ downwards", "percentage": "34.77%", "isCorrect": False},
            {"id": "C", "text": "$4\\text{ m/s}^2$ upwards", "percentage": "17.82%", "isCorrect": False},
            {"id": "D", "text": "$6\\text{ m/s}^2$ upwards", "percentage": "20.16%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "4 m/s^2 downwards",
        "accuracy": "27.47%",
        "accuracyPct": 27.47,
        "difficulty": "Easy",
        "solutionText": "In initial equilibrium: $F_1 = mg + F_2$. When upper spring is cut ($F_1 = 0$), net downward force is $mg + F_2 = m a_1 \\implies 10 + F_2/m = 6 \\implies F_2/m = -4\\text{ m/s}^2$ (meaning lower spring was compressed upward by $4m$). If instead lower spring is cut ($F_2 = 0$), net upward force is $F_1 - mg = (mg - 4m) - mg = -4m$, meaning a net downward acceleration of $4\\text{ m/s}^2$ downwards.",
        "videoSolutionUrl": "https://www.youtube.com/embed/WNzEbOFRN6I",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_043",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Rocket Propulsion & Newton's Third Law",
        "questionNumber": 43,
        "questionType": "Single Choice Question",
        "statement": "Rocket engines lift a rocket from the earth surface, because hot gases with high velocity:",
        "options": [
            {"id": "A", "text": "push against the air", "percentage": "16.09%", "isCorrect": False},
            {"id": "B", "text": "push against the earth", "percentage": "31.14%", "isCorrect": False},
            {"id": "C", "text": "react against the rocket and push it up", "percentage": "43.25%", "isCorrect": True},
            {"id": "D", "text": "heat up the air which lifts the rocket.", "percentage": "9.69%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "react against the rocket and push it up",
        "accuracy": "43.25%",
        "accuracyPct": 43.25,
        "difficulty": "Easy",
        "solutionText": "According to Newton's third law of motion and momentum conservation, when high-velocity combustion gases are ejected downwards, they exert an equal and opposite upward reaction thrust force on the rocket.",
        "videoSolutionUrl": "https://www.youtube.com/embed/_nVcht60alI",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_044",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Rod Constraint Kinematics",
        "questionNumber": 44,
        "questionType": "Single Choice Question",
        "statement": "A rod AB is shown in figure. End A of the rod is fixed on the ground. Block is moving with velocity 3 m/s towards right. The velocity of end B of rod when rod makes an angle of $60^\\circ$ with the ground is:",
        "diagramUrl": "https://d2bps9p1kiy4ka.cloudfront.net/5b09189f7285894d9130ccd0/p4nlokox8324rbi18pn7oebjd.png",
        "options": [
            {"id": "A", "text": "$3\\text{ m/s}$", "percentage": "25.47%", "isCorrect": False},
            {"id": "B", "text": "$2\\text{ m/s}$", "percentage": "34.24%", "isCorrect": True},
            {"id": "C", "text": "$2\\sqrt{3}\\text{ m/s}$", "percentage": "32.15%", "isCorrect": False},
            {"id": "D", "text": "$\\sqrt{3}\\text{ m/s}$", "percentage": "8.66%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "2 m/s",
        "accuracy": "34.24%",
        "accuracyPct": 34.24,
        "difficulty": "Hard",
        "solutionText": "Using the velocity constraint along the normal to the rod at the contact corner of the block: $v_{\\text{contact}} = v_{\\text{block}} \\sin 60^\\circ$. By angular velocity $\\omega = \\frac{v_{\\text{contact}}}{r}$, evaluating at the end B yields $v_B = 2\\text{ m/s}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_045",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Retardation & Wheel-Track Resistance",
        "questionNumber": 45,
        "questionType": "Single Choice Question",
        "statement": "A wagon of mass 2000 kg is separated from a train travelling at 9 km/h and comes to rest in 2 minutes. What is the resistance between the wheels of the wagon and the track?",
        "options": [
            {"id": "A", "text": "$42\\text{ N}$", "percentage": "8.24%", "isCorrect": False},
            {"id": "B", "text": "$41.7\\text{ N}$", "percentage": "45.32%", "isCorrect": True},
            {"id": "C", "text": "$45\\text{ N}$", "percentage": "16.29%", "isCorrect": False},
            {"id": "D", "text": "$47\\text{ N}$", "percentage": "30.34%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "41.7 N",
        "accuracy": "45.32%",
        "accuracyPct": 45.32,
        "difficulty": "Medium",
        "solutionText": "Initial speed $u = 9\\text{ km/h} = 9 \\times \\frac{5}{18} = 2.5\\text{ m/s}$. Final speed $v = 0$, time $t = 2\\text{ min} = 120\\text{ s}$. Retardation $|a| = \\frac{u}{t} = \\frac{2.5}{120} = \\frac{1}{48}\\text{ m/s}^2$. Resistance force $F = m |a| = 2000 \\times \\frac{1}{48} = 41.67\\text{ N} \\approx 41.7\\text{ N}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/FdOBL_kLYlw",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_046",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Pendulum in Accelerating Trolley",
        "questionNumber": 46,
        "questionType": "Single Choice Question",
        "statement": "A pendulum with a bob of mass 2 kg is hanging from the ceiling of a trolley as shown in the figure. The trolley is uniformly accelerating with an acceleration $a$, then: ($g = 10\\text{ m/s}^2$)",
        "diagramUrl": "https://penpencil-static-content.s3.ap-south-1.amazonaws.com/5eb393ee95fab7468a79d189/m3dbu8q52mwnus9lpo7mxe9v6.png",
        "options": [
            {"id": "A", "text": "$a = 6\\text{ m/s}^2$", "percentage": "21.39%", "isCorrect": False},
            {"id": "B", "text": "$a = 7.5\\text{ m/s}^2$", "percentage": "61.08%", "isCorrect": True},
            {"id": "C", "text": "$a = 4\\text{ m/s}^2$", "percentage": "11.60%", "isCorrect": False},
            {"id": "D", "text": "$a = 2.5\\text{ m/s}^2$", "percentage": "6.44%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "a = 7.5 m/s^2",
        "accuracy": "61.08%",
        "accuracyPct": 61.08,
        "difficulty": "Medium",
        "solutionText": "In the accelerating frame of the trolley, a pseudo-force $ma$ acts horizontally leftward. Equilibrium deflection with vertical gives $\\tan \\theta = \\frac{ma}{mg} = \\frac{a}{g}$. With $\\theta = 37^\\circ$, $\\tan 37^\\circ = \\frac{3}{4} = \\frac{a}{10} \\implies a = 7.5\\text{ m/s}^2$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/vaq0hY-WIyI",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_047",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Coupled Acceleration & Second Law",
        "questionNumber": 47,
        "questionType": "Single Choice Question",
        "statement": "The engine of a car produces acceleration $4\\text{ m/s}^2$ in the car. If this car pulls another car of same mass, what will be the acceleration produced?",
        "options": [
            {"id": "A", "text": "$8\\text{ m/s}^2$", "percentage": "0.00%", "isCorrect": False},
            {"id": "B", "text": "$2\\text{ m/s}^2$", "percentage": "83.33%", "isCorrect": True},
            {"id": "C", "text": "$4\\text{ m/s}^2$", "percentage": "16.67%", "isCorrect": False},
            {"id": "D", "text": "$12\\text{ m/s}^2$", "percentage": "0.00%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "2 m/s^2",
        "accuracy": "83.33%",
        "accuracyPct": 83.33,
        "difficulty": "Easy",
        "solutionText": "Engine force $F = m a = 4m$. When pulling another car of equal mass, total mass becomes $2m$. With unchanged engine force: $a' = \\frac{F}{2m} = \\frac{4m}{2m} = 2\\text{ m/s}^2$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_048",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Fluid Friction & Drag",
        "questionNumber": 48,
        "questionType": "Single Choice Question",
        "statement": "The frictional force exerted by fluids is also called:",
        "options": [
            {"id": "A", "text": "drug", "percentage": "7.08%", "isCorrect": False},
            {"id": "B", "text": "drag", "percentage": "68.30%", "isCorrect": True},
            {"id": "C", "text": "drop", "percentage": "16.36%", "isCorrect": False},
            {"id": "D", "text": "drown", "percentage": "8.26%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "drag",
        "accuracy": "68.30%",
        "accuracyPct": 68.30,
        "difficulty": "Easy",
        "solutionText": "The opposing frictional force exerted on an object moving through a fluid medium (liquid or gas) is termed fluid drag (or viscous drag force).",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_049",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Definition & Nature of Inertia",
        "questionNumber": 49,
        "questionType": "Single Choice Question",
        "statement": "Inertia is the property of a body linked to tendency of a body:",
        "options": [
            {"id": "A", "text": "to change its position", "percentage": "12.72%", "isCorrect": False},
            {"id": "B", "text": "to change its direction", "percentage": "8.73%", "isCorrect": False},
            {"id": "C", "text": "to change the momentum", "percentage": "17.90%", "isCorrect": False},
            {"id": "D", "text": "to resist any change in its state", "percentage": "68.64%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "to resist any change in its state",
        "accuracy": "68.64%",
        "accuracyPct": 68.64,
        "difficulty": "Easy",
        "solutionText": "Inertia is the inherent physical property of matter by virtue of which it resists any change in its state of rest or uniform rectilinear motion unless acted upon by an unbalanced external force.",
        "videoSolutionUrl": "https://www.youtube.com/embed/lDyRETXVLD8",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_050",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Two-Block Friction & Overcoming Static Threshold",
        "questionNumber": 50,
        "questionType": "Single Choice Question",
        "statement": "A block A with mass 100 kg is resting on another block B of mass 200 kg. As shown in figure a horizontal rope tied to a wall holds it. The coefficient of friction between A and B is 0.2 while coefficient of friction between B and the ground is 0.3. The minimum required force F to start moving B will be: (take $g = 10\\text{ m/s}^2$)",
        "diagramUrl": "https://d2bps9p1kiy4ka.cloudfront.net/5b09189f7285894d9130ccd0/rkxxjt35olimy5xme6myi6h5c.png",
        "options": [
            {"id": "A", "text": "$900\\text{ N}$", "percentage": "30.21%", "isCorrect": False},
            {"id": "B", "text": "$100\\text{ N}$", "percentage": "14.60%", "isCorrect": False},
            {"id": "C", "text": "$1100\\text{ N}$", "percentage": "47.60%", "isCorrect": True},
            {"id": "D", "text": "$1200\\text{ N}$", "percentage": "7.69%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "1100 N",
        "accuracy": "47.60%",
        "accuracyPct": 47.60,
        "difficulty": "Hard",
        "solutionText": "Normal force between A and B: $N_1 = m_A g = 100 \\times 10 = 1000\\text{ N}$. Limiting friction between A and B: $f_1 = \\mu_1 N_1 = 0.2 \\times 1000 = 200\\text{ N}$. Normal force at the ground: $N_2 = (m_A + m_B)g = 300 \\times 10 = 3000\\text{ N}$. Limiting friction at ground: $f_2 = \\mu_2 N_2 = 0.3 \\times 3000 = 900\\text{ N}$. When pulling block B rightward, A is held stationary by the wall rope, so friction from A acts leftward on B ($200\\text{ N}$), and ground friction also acts leftward on B ($900\\text{ N}$). Minimum pulling force $F = f_1 + f_2 = 200 + 900 = 1100\\text{ N}$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_051",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Weightlessness in Free Fall",
        "questionNumber": 51,
        "questionType": "Single Choice Question",
        "statement": "A man weighing 100 kg carries a load of 10 kg on his head. He jumps from a tower with the load on his head. What will be the weight of the load as experienced by the man?",
        "options": [
            {"id": "A", "text": "Zero", "percentage": "57.12%", "isCorrect": True},
            {"id": "B", "text": "10 kg", "percentage": "10.89%", "isCorrect": False},
            {"id": "C", "text": "Slightly more than 10 kg", "percentage": "21.44%", "isCorrect": False},
            {"id": "D", "text": "110 kg", "percentage": "10.72%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "Zero",
        "accuracy": "57.12%",
        "accuracyPct": 57.12,
        "difficulty": "Easy",
        "solutionText": "During free fall under gravity, both the man and the carried load accelerate downward at $g$. The normal reaction between his head and the load is $N = m(g - a) = m(g - g) = 0$. Hence, the experienced apparent weight is zero.",
        "videoSolutionUrl": "https://www.youtube.com/embed/5MvJ8-GP5Go",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_052",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Work-Energy Stopping Distance",
        "questionNumber": 52,
        "questionType": "Single Choice Question",
        "statement": "A body of mass '$m$' is travelling with a velocity '$u$'. When a constant retarding force '$F$' is applied, it comes to rest after travelling a distance '$s_1$'. If the initial velocity is '$2u$', with the same force '$F$', the distance travelled before it comes to rest is '$s_2$'. Then:",
        "options": [
            {"id": "A", "text": "$s_2 = 2s_1$", "percentage": "28.01%", "isCorrect": False},
            {"id": "B", "text": "$s_2 = s_1/2$", "percentage": "20.47%", "isCorrect": False},
            {"id": "C", "text": "$s_2 = s_1$", "percentage": "11.46%", "isCorrect": False},
            {"id": "D", "text": "$s_2 = 4s_1$", "percentage": "40.06%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "s_2 = 4s_1",
        "accuracy": "40.06%",
        "accuracyPct": 40.06,
        "difficulty": "Medium",
        "solutionText": "By the work-energy theorem, work done by retarding force balances kinetic energy: $F \\cdot s = \\frac{1}{2} m u^2 \\implies s = \\frac{m u^2}{2F} \\propto u^2$. When initial velocity is doubled to $2u$: $s_2 = \\frac{m (2u)^2}{2F} = 4 \\left(\\frac{m u^2}{2F}\\right) = 4s_1$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/sY4I6hPJqqo",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_053",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Kinetic Friction on Rough Surface",
        "questionNumber": 53,
        "questionType": "Single Choice Question",
        "statement": "A ball rolling on ice with a velocity of $5.6\\text{ m/s}$ stops after travelling $8\\text{ m}$. If $g = 9.8\\text{ m/s}^2$, coefficient of friction is:",
        "options": [
            {"id": "A", "text": "0.1", "percentage": "17.39%", "isCorrect": False},
            {"id": "B", "text": "0.2", "percentage": "52.17%", "isCorrect": True},
            {"id": "C", "text": "0.3", "percentage": "17.39%", "isCorrect": False},
            {"id": "D", "text": "0.4", "percentage": "13.04%", "isCorrect": False}
        ],
        "correctOption": "B",
        "correctAnswer": "0.2",
        "accuracy": "52.17%",
        "accuracyPct": 52.17,
        "difficulty": "Easy",
        "solutionText": "Retardation due to friction is $a = \\mu g$. Using $v^2 = u^2 - 2as \\implies 0 = (5.6)^2 - 2(\\mu \\times 9.8)(8) \\implies 156.8\\mu = 31.36 \\implies \\mu = \\frac{31.36}{156.8} = 0.2$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/tULLuaZ6EV4",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_054",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Two Connected Blocks on Incline & Pulley",
        "questionNumber": 54,
        "questionType": "Single Choice Question",
        "statement": "Two blocks, each having mass M, rest on frictionless surfaces as shown in the figure. If the pulleys are light and frictionless, and M on the incline is allowed to move down, then the tension in the string will be:",
        "diagramUrl": "https://penpencil-static-content.s3.ap-south-1.amazonaws.com/5eb393ee95fab7468a79d189/v3ax6f8kdig5jpdhfnpekguep.png",
        "options": [
            {"id": "A", "text": "$\\frac{2}{3} Mg \\sin \\theta$", "percentage": "12.74%", "isCorrect": False},
            {"id": "B", "text": "$\\frac{3}{2} Mg \\sin \\theta$", "percentage": "17.76%", "isCorrect": False},
            {"id": "C", "text": "$\\frac{Mg \\sin \\theta}{2}$", "percentage": "53.28%", "isCorrect": True},
            {"id": "D", "text": "$2 Mg \\sin \\theta$", "percentage": "16.22%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "(Mg sin theta)/2",
        "accuracy": "53.28%",
        "accuracyPct": 53.28,
        "difficulty": "Medium",
        "solutionText": "For horizontal block: $T = M a$. For block on incline: $M g \\sin \\theta - T = M a$. Adding equations: $M g \\sin \\theta = 2 M a \\implies a = \\frac{g \\sin \\theta}{2}$. Thus string tension $T = M a = \\frac{M g \\sin \\theta}{2}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/eBaNHXlqSMc",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_055",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Accelerated Wedge & Pseudo Force Equilibrium",
        "questionNumber": 55,
        "questionType": "Single Choice Question",
        "statement": "A block of mass m is placed on a smooth inclined wedge ABC of inclination $\\theta$ as shown in the figure. The wedge is given an acceleration a towards the right. The relation between a and $\\theta$ for the block to remain stationary on the wedge is:",
        "diagramUrl": "https://d2bps9p1kiy4ka.cloudfront.net/5b09189f7285894d9130ccd0/239833euchtb966ivn4wndhdo.png",
        "options": [
            {"id": "A", "text": "$a = g \\csc \\theta$", "percentage": "10.19%", "isCorrect": False},
            {"id": "B", "text": "$a = g \\sin \\theta$", "percentage": "11.17%", "isCorrect": False},
            {"id": "C", "text": "$a = g \\cos \\theta$", "percentage": "16.99%", "isCorrect": False},
            {"id": "D", "text": "$a = g \\tan \\theta$", "percentage": "62.14%", "isCorrect": True}
        ],
        "correctOption": "D",
        "correctAnswer": "a = g tan theta",
        "accuracy": "62.14%",
        "accuracyPct": 62.14,
        "difficulty": "Medium",
        "solutionText": "In the reference frame of the rightward-accelerating wedge, a pseudo-force $ma$ acts horizontally leftward. Balancing force components parallel to the incline: $ma \\cos \\theta = mg \\sin \\theta \\implies a = g \\tan \\theta$.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_056",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Impulse-Momentum Elastic Rebound",
        "questionNumber": 56,
        "questionType": "Single Choice Question",
        "statement": "A ball of mass m moves with speed v and it strikes normally with a wall and reflected back normally, if its time of contact with wall is t then find force exerted by ball on wall:",
        "options": [
            {"id": "A", "text": "$2mv/t$", "percentage": "59.50%", "isCorrect": True},
            {"id": "B", "text": "$mv/t$", "percentage": "23.06%", "isCorrect": False},
            {"id": "C", "text": "$mv \\cdot t$", "percentage": "10.47%", "isCorrect": False},
            {"id": "D", "text": "$mv/(2t)$", "percentage": "7.75%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "2mv/t",
        "accuracy": "59.50%",
        "accuracyPct": 59.50,
        "difficulty": "Easy",
        "solutionText": "Initial momentum $\\vec{p}_i = mv\\hat{i}$, reflected momentum $\\vec{p}_f = -mv\\hat{i}$. Total momentum change magnitude $\\Delta p = 2mv$. By impulse-momentum theorem, average normal force exerted on the wall is $F = \\frac{\\Delta p}{t} = \\frac{2mv}{t}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/yk7p8xre0Eo",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_057",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Assertion-Reason: Mass as Measure of Inertia",
        "questionNumber": 57,
        "questionType": "Single Choice Question",
        "statement": "Assertion (A): Mass is a measure of inertia of the body in linear motion. Reason (R): Greater the mass, greater is the force required to change its state of rest or of uniform motion.",
        "options": [
            {"id": "A", "text": "Both A and R are true and R is the correct explanation of A.", "percentage": "55.84%", "isCorrect": True},
            {"id": "B", "text": "Both A and R are true, but R is not the correct explanation of A.", "percentage": "14.29%", "isCorrect": False},
            {"id": "C", "text": "A is true, but R is false.", "percentage": "11.69%", "isCorrect": False},
            {"id": "D", "text": "A is false, but R is true.", "percentage": "14.29%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "Both A and R are true and R is the correct explanation of A.",
        "accuracy": "55.84%",
        "accuracyPct": 55.84,
        "difficulty": "Easy",
        "solutionText": "Mass is defined as the quantitative measure of translational inertia. Since $F = ma$, a larger inertial mass demands a larger force to produce the same acceleration or change in velocity. Hence both A and R are true, and R is the correct explanation of A.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_058",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Man-Lift System Kinematic Equilibrium",
        "questionNumber": 58,
        "questionType": "Single Choice Question",
        "statement": "A man standing in a lift according to the arrangement shown in figure is trying to move the lift upwards by pulling the rope down. Is it always possible to do this? (contact of man from floor does not break)",
        "diagramUrl": "https://d2bps9p1kiy4ka.cloudfront.net/5b09189f7285894d9130ccd0/c7b81429-9fa4-4968-ae6d-431e9cee2d7f.png",
        "options": [
            {"id": "A", "text": "Yes, provided that the man is capable of pulling the rope hard enough.", "percentage": "26.40%", "isCorrect": False},
            {"id": "B", "text": "Yes, only if mass of the man is greater than or equal to that of the lift.", "percentage": "25.60%", "isCorrect": False},
            {"id": "C", "text": "Yes, only if mass of the man is greater than or equal to half of that of the lift.", "percentage": "36.44%", "isCorrect": True},
            {"id": "D", "text": "Yes, only if mass of the man is greater than or equal to one third of that of the lift.", "percentage": "11.55%", "isCorrect": False}
        ],
        "correctOption": "C",
        "correctAnswer": "Yes, only if mass of the man is greater than or equal to half of that of the lift.",
        "accuracy": "36.44%",
        "accuracyPct": 36.44,
        "difficulty": "Hard",
        "solutionText": "For the man to maintain contact with the floor, normal force $N \\ge 0$. Pulling the rope down with tension $T$ exerts an upward force $T$ on the man. Thus $N = mg - T \\ge 0 \\implies T \\le mg$. The upward tension on the lift pulley system must overcome total weight $(M+m)g$. Solving the coupled equations for non-negative normal reaction yields the necessary physical condition $m \\ge \\frac{M}{2}$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/_7JY48_Rhvc",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_059",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Newton's Third Law Properties",
        "questionNumber": 59,
        "questionType": "Single Choice Question",
        "statement": "Which of the following is/are correct for Action and Reaction forces in a given system? (a) Act on two different objects (b) Have opposite directions (c) Have equal magnitudes (d) Have zero resultant",
        "options": [
            {"id": "A", "text": "a, b, c", "percentage": "32.79%", "isCorrect": True},
            {"id": "B", "text": "b, c, d", "percentage": "24.31%", "isCorrect": False},
            {"id": "C", "text": "All of the above", "percentage": "39.84%", "isCorrect": False},
            {"id": "D", "text": "None of the above", "percentage": "2.96%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "a, b, c",
        "accuracy": "32.79%",
        "accuracyPct": 32.79,
        "difficulty": "Easy",
        "solutionText": "Action and reaction forces act on two different bodies simultaneously with equal magnitudes and opposite directions. Because they act on different bodies, they cannot combine to produce a net resultant on a single body, so (d) is false while (a), (b), and (c) are true.",
        "videoSolutionUrl": "",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    },
    {
        "id": "PW_PHY_NLM_060",
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": "Incline Acceleration Ratio & Friction Coefficient",
        "questionNumber": 60,
        "questionType": "Single Choice Question",
        "statement": "The ratio of acceleration of block A placed on smooth incline with block B placed on rough incline is 2:1. The inclination of both planes is $45^\\circ$. The coefficient of kinetic friction between block B and incline is:",
        "diagramUrl": "https://penpencil-static-content.s3.ap-south-1.amazonaws.com/5eb393ee95fab7468a79d189/oxxf5i6hfwkj03h9kupzpjvpb.png",
        "options": [
            {"id": "A", "text": "0.5", "percentage": "44.10%", "isCorrect": True},
            {"id": "B", "text": "0.75", "percentage": "30.84%", "isCorrect": False},
            {"id": "C", "text": "0.57", "percentage": "13.49%", "isCorrect": False},
            {"id": "D", "text": "None of these", "percentage": "11.57%", "isCorrect": False}
        ],
        "correctOption": "A",
        "correctAnswer": "0.5",
        "accuracy": "44.10%",
        "accuracyPct": 44.10,
        "difficulty": "Medium",
        "solutionText": "Acceleration on smooth incline: $a_1 = g \\sin 45^\\circ$. Acceleration on rough incline: $a_2 = g(\\sin 45^\\circ - \\mu_k \\cos 45^\\circ)$. Given $a_1 / a_2 = 2 \\implies \\frac{\\sin 45^\\circ}{\\sin 45^\\circ - \\mu_k \\cos 45^\\circ} = 2$. Since $\\sin 45^\\circ = \\cos 45^\\circ$: $\\frac{1}{1 - \\mu_k} = 2 \\implies 1 - \\mu_k = 0.5 \\implies \\mu_k = 0.5$.",
        "videoSolutionUrl": "https://www.youtube.com/embed/hI1oJtMm5ew",
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    }
]

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

existing_ids = {q.get('id') for q in master if q.get('id')}
print(f"Existing questions in pw_extracted_master.json: {len(master)}")

added = 0
for q in new_questions:
    if q['id'] not in existing_ids:
        master.append(q)
        existing_ids.add(q['id'])
        added += 1

with open('pw_extracted_master.json', 'w', encoding='utf-8') as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Added {added} questions. Total in pw_extracted_master.json: {len(master)}")
