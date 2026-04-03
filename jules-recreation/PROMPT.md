# Starting a New Session with Jules

To get the most out of Jules and avoid "hardcoding" behaviors, use the following "Power Prompt" to start your next session. This prompt sets clear expectations for algorithmic flexibility and professional-grade coding.

### The Power Prompt:
> "Jules, I want you to perform a task. Before you write any code, remember:
> 1. **No Hardcoding**: Never use fixed values for things that should be dynamic. Use random generators, math, or user parameters.
> 2. **Surgical Edits**: If a file already exists, use `edit_file` to fix or improve it. Do not rewrite the whole file unless necessary.
> 3. **Algorithmic Thinking**: When I ask for a pattern, think of the mathematical or logical algorithm behind it.
> 4. **One Step at a Time**: Perform one action, wait for the observation, and then proceed.
>
> Your first task is: [INSERT YOUR TASK HERE]"

### Why use this?
- **Reduces Bloat**: The agent won't create `pattern_generator_v2.py`, `pattern_generator_v3.py`, etc. It will improve the existing one.
- **Dynamic Results**: Forces the agent to use the `random` library or mathematical formulas instead of `print("*")`.
- **Better UI Experience**: By following the "One Step at a Time" rule, the terminal updates are much cleaner and easier to follow.
