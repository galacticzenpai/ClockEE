/**
 * ClockEE Package Wrapper: Agent Memory Client (JavaScript)
 * Client-side interface to store and retrieve persistent memory nodes.
 */

window.ClockEE_Memory = {
  storageKey: "clockee_agent_memory_cache",

  /**
   * Remember an item in local agent memory.
   * @param {string} key 
   * @param {any} value 
   * @param {string} category 
   */
  remember(key, value, category = "general") {
    try {
      const data = JSON.parse(localStorage.getItem(this.storageKey) || "{}");
      data[key] = {
        value,
        category,
        timestamp: new Date().toISOString()
      };
      localStorage.setItem(this.storageKey, JSON.stringify(data));
      console.log(`[AgentMemory] Remembered: [${category}] ${key}`);
      return true;
    } catch (e) {
      console.error("[AgentMemory] Failed to save memory", e);
      return false;
    }
  },

  /**
   * Recall a specific memory node.
   * @param {string} key 
   */
  recall(key) {
    try {
      const data = JSON.parse(localStorage.getItem(this.storageKey) || "{}");
      return data[key] ? data[key].value : null;
    } catch (e) {
      return null;
    }
  },

  /**
   * Retrieve all memories under a specific category.
   * @param {string} category 
   */
  getAll(category = null) {
    try {
      const data = JSON.parse(localStorage.getItem(this.storageKey) || "{}");
      if (!category) return data;
      const filtered = {};
      for (const [k, v] of Object.entries(data)) {
        if (v.category === category) filtered[k] = v.value;
      }
      return filtered;
    } catch (e) {
      return {};
    }
  }
};
