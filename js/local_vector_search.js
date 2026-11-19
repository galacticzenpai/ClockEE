/**
 * ⚡ ClockEE — Reel #5: Client-Side Local Vector Search Engine (js/local_vector_search.js)
 * Local-First In-Browser Vector Cosine Similarity Search for JEE Practice Questions.
 */

(function(window) {
  'use strict';

  const VECTOR_DIM = 64;

  // Simple, deterministic in-browser pseudo-embedding generator
  function generateVector(text, subject) {
    const vec = new Float32Array(VECTOR_DIM);
    const sub = (subject || 'Physics').toLowerCase();
    
    // Seed with subject
    let hash = 0;
    for (let i = 0; i < sub.length; i++) hash = (hash << 5) - hash + sub.charCodeAt(i);
    for (let i = 0; i < VECTOR_DIM; i++) {
      vec[i] = Math.sin((i + 1) * Math.abs(hash % 100) / 10.0);
    }

    // Add token features
    const words = (text || '').toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(Boolean);
    words.forEach(w => {
      let wh = 0;
      for (let j = 0; j < w.length; j++) wh = (wh << 5) - wh + w.charCodeAt(j);
      const idx = Math.abs(wh) % VECTOR_DIM;
      vec[idx] += 1.5;
      vec[(idx + 1) % VECTOR_DIM] += 0.8;
      vec[(idx - 1 + VECTOR_DIM) % VECTOR_DIM] += 0.8;
    });

    // L2 Normalize
    let norm = 0;
    for (let i = 0; i < VECTOR_DIM; i++) norm += vec[i] * vec[i];
    norm = Math.sqrt(norm);
    if (norm > 0) {
      for (let i = 0; i < VECTOR_DIM; i++) vec[i] /= norm;
    }
    return vec;
  }

  function cosineSim(v1, v2) {
    let dot = 0;
    for (let i = 0; i < VECTOR_DIM; i++) dot += v1[i] * v2[i];
    return dot;
  }

  class LocalVectorSearch {
    constructor() {
      this.corpus = [];
      this.isReady = false;
      this.init();
    }

    init() {
      // Default core concepts
      const sampleConcepts = [
        { id: "vss_phy_01", subject: "Physics", topic: "Rotational Dynamics", snippet: "Calculate torque and moment of inertia for rolling cylinder without slipping." },
        { id: "vss_phy_02", subject: "Physics", topic: "Electrostatics", snippet: "Determine electric field intensity on the axis of charged circular ring." },
        { id: "vss_phy_03", subject: "Physics", topic: "Electromagnetic Induction", snippet: "Motional EMF induced in rotating copper disc in uniform magnetic field." },
        { id: "vss_chem_01", subject: "Chemistry", topic: "Chemical Kinetics", snippet: "First-order reaction rate constant variation with activation energy." },
        { id: "vss_chem_02", subject: "Chemistry", topic: "Coordination Compounds", snippet: "Crystal field splitting energy of octahedral complex with strong field ligands." },
        { id: "vss_math_01", subject: "Maths", topic: "Calculus", snippet: "Definite integration using reduction formula and Leibniz rule differentiation." },
        { id: "vss_math_02", subject: "Maths", topic: "Coordinate Geometry", snippet: "Equation of tangent and normal to hyperbola passing through given point." }
      ];

      this.corpus = sampleConcepts.map(item => ({
        ...item,
        vec: generateVector(item.snippet, item.subject)
      }));
      this.isReady = true;
    }

    findSimilar(query, subject = null, topK = 3) {
      const t0 = performance.now();
      const qVec = generateVector(query, subject);
      
      const filtered = subject 
        ? this.corpus.filter(c => c.subject.toLowerCase() === subject.toLowerCase()) 
        : this.corpus;

      const scored = filtered.map(item => ({
        id: item.id,
        subject: item.subject,
        topic: item.topic,
        snippet: item.snippet,
        score: Math.round(cosineSim(qVec, item.vec) * 1000) / 1000
      }));

      scored.sort((a, b) => b.score - a.score);
      const topResults = scored.slice(0, topK);
      const latencyMs = Math.round((performance.now() - t0) * 100) / 100;

      return {
        query,
        latencyMs,
        results: topResults
      };
    }
  }

  // Export to global scope
  window.ClockEELocalVSS = new LocalVectorSearch();

})(typeof window !== 'undefined' ? window : this);
