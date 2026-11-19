/**
 * ClockEE OS 2.0 - 75-Chapter PCM Syllabus Matrix
 * Official JEE (Main & Advanced) Syllabus breakdown:
 * 25 Physics + 25 Chemistry + 25 Mathematics = 75 Total Chapters
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.SyllabusData = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const CHAPTERS = [
    // Physics (25)
    { id: 1, subject: 'Physics', title: 'Units, Dimensions & Errors', weightage: 'Medium', classGrade: 11 },
    { id: 2, subject: 'Physics', title: 'Kinematics in 1D & 2D (Vectors)', weightage: 'High', classGrade: 11 },
    { id: 3, subject: 'Physics', title: "Newton's Laws of Motion & Friction", weightage: 'High', classGrade: 11 },
    { id: 4, subject: 'Physics', title: 'Work, Energy & Power', weightage: 'High', classGrade: 11 },
    { id: 5, subject: 'Physics', title: 'Circular Motion', weightage: 'Medium', classGrade: 11 },
    { id: 6, subject: 'Physics', title: 'Center of Mass & Linear Momentum', weightage: 'High', classGrade: 11 },
    { id: 7, subject: 'Physics', title: 'Rotational Dynamics & Moment of Inertia', weightage: 'High', classGrade: 11 },
    { id: 8, subject: 'Physics', title: 'Gravitation', weightage: 'High', classGrade: 11 },
    { id: 9, subject: 'Physics', title: 'Thermal Properties & Thermodynamics', weightage: 'High', classGrade: 11 },
    { id: 10, subject: 'Physics', title: 'Kinetic Theory of Gases', weightage: 'Medium', classGrade: 11 },
    { id: 11, subject: 'Physics', title: 'Oscillations (SHM)', weightage: 'High', classGrade: 11 },
    { id: 12, subject: 'Physics', title: 'Wave Motion & Acoustics', weightage: 'Medium', classGrade: 11 },
    { id: 13, subject: 'Physics', title: 'Electrostatics & Electric Potential', weightage: 'High', classGrade: 12 },
    { id: 14, subject: 'Physics', title: 'Capacitance & Dielectrics', weightage: 'Medium', classGrade: 12 },
    { id: 15, subject: 'Physics', title: 'Current Electricity', weightage: 'High', classGrade: 12 },
    { id: 16, subject: 'Physics', title: 'Magnetic Effects of Current', weightage: 'High', classGrade: 12 },
    { id: 17, subject: 'Physics', title: 'Magnetism & Matter', weightage: 'Low', classGrade: 12 },
    { id: 18, subject: 'Physics', title: 'Electromagnetic Induction', weightage: 'High', classGrade: 12 },
    { id: 19, subject: 'Physics', title: 'Alternating Current', weightage: 'Medium', classGrade: 12 },
    { id: 20, subject: 'Physics', title: 'Electromagnetic Waves', weightage: 'Medium', classGrade: 12 },
    { id: 21, subject: 'Physics', title: 'Ray Optics & Optical Instruments', weightage: 'High', classGrade: 12 },
    { id: 22, subject: 'Physics', title: 'Wave Optics', weightage: 'Medium', classGrade: 12 },
    { id: 23, subject: 'Physics', title: 'Dual Nature of Radiation & Matter', weightage: 'High', classGrade: 12 },
    { id: 24, subject: 'Physics', title: 'Atoms & Nuclei', weightage: 'High', classGrade: 12 },
    { id: 25, subject: 'Physics', title: 'Semiconductor Electronics', weightage: 'High', classGrade: 12 },

    // Chemistry (25)
    { id: 26, subject: 'Chemistry', title: 'Mole Concept & Stoichiometry', weightage: 'Medium', classGrade: 11 },
    { id: 27, subject: 'Chemistry', title: 'Atomic Structure', weightage: 'High', classGrade: 11 },
    { id: 28, subject: 'Chemistry', title: 'Chemical Bonding & Molecular Structure', weightage: 'High', classGrade: 11 },
    { id: 29, subject: 'Chemistry', title: 'Chemical Thermodynamics', weightage: 'High', classGrade: 11 },
    { id: 30, subject: 'Chemistry', title: 'Chemical & Ionic Equilibrium', weightage: 'High', classGrade: 11 },
    { id: 31, subject: 'Chemistry', title: 'Redox Reactions & Electrochemistry', weightage: 'High', classGrade: 11 },
    { id: 32, subject: 'Chemistry', title: 'Periodic Properties & Classification', weightage: 'High', classGrade: 11 },
    { id: 33, subject: 'Chemistry', title: 'General Organic Chemistry (GOC)', weightage: 'High', classGrade: 11 },
    { id: 34, subject: 'Chemistry', title: 'Hydrocarbons (Alkanes, Alkenes, Alkynes)', weightage: 'High', classGrade: 11 },
    { id: 35, subject: 'Chemistry', title: 'Solutions & Colligative Properties', weightage: 'High', classGrade: 12 },
    { id: 36, subject: 'Chemistry', title: 'Chemical Kinetics', weightage: 'High', classGrade: 12 },
    { id: 37, subject: 'Chemistry', title: 'Surface Chemistry', weightage: 'Low', classGrade: 12 },
    { id: 38, subject: 'Chemistry', title: 'd and f-Block Elements', weightage: 'High', classGrade: 12 },
    { id: 39, subject: 'Chemistry', title: 'Coordination Compounds', weightage: 'High', classGrade: 12 },
    { id: 40, subject: 'Chemistry', title: 'p-Block Elements (Grp 13-18)', weightage: 'Medium', classGrade: 12 },
    { id: 41, subject: 'Chemistry', title: 'Haloalkanes & Haloarenes', weightage: 'Medium', classGrade: 12 },
    { id: 42, subject: 'Chemistry', title: 'Alcohols, Phenols & Ethers', weightage: 'High', classGrade: 12 },
    { id: 43, subject: 'Chemistry', title: 'Aldehydes, Ketones & Carboxylic Acids', weightage: 'High', classGrade: 12 },
    { id: 44, subject: 'Chemistry', title: 'Amines & Diazonium Salts', weightage: 'High', classGrade: 12 },
    { id: 45, subject: 'Chemistry', title: 'Biomolecules', weightage: 'High', classGrade: 12 },
    { id: 46, subject: 'Chemistry', title: 'Polymers & Everyday Chemistry', weightage: 'Low', classGrade: 12 },
    { id: 47, subject: 'Chemistry', title: 'Practical Chemistry & Salt Analysis', weightage: 'Medium', classGrade: 12 },
    { id: 48, subject: 'Chemistry', title: 'Environmental Chemistry', weightage: 'Low', classGrade: 11 },
    { id: 49, subject: 'Chemistry', title: 'Solid State (Select Principles)', weightage: 'Low', classGrade: 12 },
    { id: 50, subject: 'Chemistry', title: 'Purification of Organic Compounds', weightage: 'Medium', classGrade: 11 },

    // Mathematics (25)
    { id: 51, subject: 'Mathematics', title: 'Sets, Relations & Functions', weightage: 'High', classGrade: 11 },
    { id: 52, subject: 'Mathematics', title: 'Complex Numbers & Quadratic Equations', weightage: 'High', classGrade: 11 },
    { id: 53, subject: 'Mathematics', title: 'Matrices & Determinants', weightage: 'High', classGrade: 12 },
    { id: 54, subject: 'Mathematics', title: 'Permutations & Combinations', weightage: 'Medium', classGrade: 11 },
    { id: 55, subject: 'Mathematics', title: 'Binomial Theorem', weightage: 'High', classGrade: 11 },
    { id: 56, subject: 'Mathematics', title: 'Sequences & Series (AP, GP, HP)', weightage: 'High', classGrade: 11 },
    { id: 57, subject: 'Mathematics', title: 'Limits, Continuity & Differentiability', weightage: 'High', classGrade: 12 },
    { id: 58, subject: 'Mathematics', title: 'Application of Derivatives (AOD)', weightage: 'High', classGrade: 12 },
    { id: 59, subject: 'Mathematics', title: 'Indefinite Integration', weightage: 'Medium', classGrade: 12 },
    { id: 60, subject: 'Mathematics', title: 'Definite Integration & Area Under Curves', weightage: 'High', classGrade: 12 },
    { id: 61, subject: 'Mathematics', title: 'Differential Equations', weightage: 'High', classGrade: 12 },
    { id: 62, subject: 'Mathematics', title: 'Straight Lines & Pair of Lines', weightage: 'High', classGrade: 11 },
    { id: 63, subject: 'Mathematics', title: 'Circles', weightage: 'High', classGrade: 11 },
    { id: 64, subject: 'Mathematics', title: 'Parabola', weightage: 'Medium', classGrade: 11 },
    { id: 65, subject: 'Mathematics', title: 'Ellipse & Hyperbola', weightage: 'High', classGrade: 11 },
    { id: 66, subject: 'Mathematics', title: 'Vector Algebra', weightage: 'High', classGrade: 12 },
    { id: 67, subject: 'Mathematics', title: 'Three Dimensional Geometry (3D)', weightage: 'High', classGrade: 12 },
    { id: 68, subject: 'Mathematics', title: 'Probability', weightage: 'High', classGrade: 12 },
    { id: 69, subject: 'Mathematics', title: 'Statistics', weightage: 'High', classGrade: 11 },
    { id: 70, subject: 'Mathematics', title: 'Trigonometric Ratios & Equations', weightage: 'Medium', classGrade: 11 },
    { id: 71, subject: 'Mathematics', title: 'Inverse Trigonometric Functions', weightage: 'Medium', classGrade: 12 },
    { id: 72, subject: 'Mathematics', title: 'Mathematical Reasoning', weightage: 'Low', classGrade: 11 },
    { id: 73, subject: 'Mathematics', title: 'Linear Inequalities', weightage: 'Low', classGrade: 11 },
    { id: 74, subject: 'Mathematics', title: 'Properties of Triangles', weightage: 'Low', classGrade: 11 },
    { id: 75, subject: 'Mathematics', title: 'Heights & Distances', weightage: 'Low', classGrade: 11 }
  ];

  return {
    CHAPTERS,
    getChaptersBySubject: (sub) => CHAPTERS.filter(c => c.subject.toLowerCase() === sub.toLowerCase()),
    getChapterById: (id) => CHAPTERS.find(c => c.id === Number(id))
  };
});
