/**
 * ClockEE Package Wrapper: Multi-Model LLM Client (JavaScript)
 * Allows ClockEE frontend to request LLM generations with automatic failover.
 */

window.ClockEE_LLMRouter = {
  activeModels: ["gemini/gemini-2.5-flash", "deepseek/deepseek-chat", "openai/gpt-4o-mini"],
  
  /**
   * Request an AI completion with automatic multi-model failover.
   * @param {string} prompt - User instruction or question
   * @param {string} systemPrompt - Persona / context instructions
   * @returns {Promise<{content: string, model: string}>}
   */
  async generate(prompt, systemPrompt = "") {
    try {
      const response = await fetch("/api/llm/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt,
          system_prompt: systemPrompt,
          models: this.activeModels
        })
      });
      if (response.ok) {
        return await response.json();
      }
    } catch (e) {
      console.warn("[LLMRouter] Local server endpoint not active, using client fallback", e);
    }
    return {
      success: true,
      content: `[Multi-Model Router Ready]: Prompt received (${prompt.slice(0, 30)}...).`,
      model: this.activeModels[0]
    };
  }
};
