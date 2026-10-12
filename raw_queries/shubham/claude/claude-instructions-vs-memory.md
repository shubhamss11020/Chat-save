---
conversation_id: 2eb68f11-6903-40d6-834f-b9b42a39a6f5
platform: claude
username: "shubham"
title: "Claude instructions vs memory"
created_at: "2026-10-09T15:01:38.182927Z"
updated_at: "2026-10-12 10:35:35 EDT"
---

# Claude instructions vs memory

## User (2026-10-12 10:35:35 EDT)

what is the differnence of instruction and memory in claude, instruction is something that claude executes and hardcoded and memory is something claude updates about us as we continues to use the claude and chat with it, correct me and teach me

## Claude (2026-10-12 10:35:35 EDT)

You're mostly right, with a few corrections.

**Instructions**
- Written by you (or your organization), not learned by Claude.
- Examples: Project instructions, custom instructions, a skill, your preferences settings ("always reply in bullet points").
- Claude reads them at the start of a conversation and follows them as guidance.
- They only change when *you* edit them.
- Correction: "hardcoded" is a bit too strong. They're text placed in Claude's context, so Claude follows them very reliably, but they aren't code. If an instruction conflicts with safety rules or with something you ask later, Claude uses judgment. Instructions are also usually scoped: a Project's instructions apply only inside that Project.

**Memory**
- Information Claude has saved about you and your work from past chats: your role, ongoing projects, preferences, people you work with.
- It's built in two ways: automatically from your conversations (when "Generate memory from chats" is on), and when you say "remember that...".
- It's stored as notes that get loaded into new conversations, so Claude doesn't start from zero.
- Correction: Claude doesn't "learn" in the sense of its underlying model changing. The model stays the same. Memory is just saved notes inserted into the conversation. Also, Claude is selective: it only files durable facts (not every passing comment), and it uses a memory only when it's relevant to what you're asking.

**Key differences**

| | Instructions | Memory |
|---|---|---|
| Who writes it | You | Mostly Claude (from chats), or you on request |
| Changes | Only when you edit | Updates as you keep chatting |
| Purpose | "Do it this way" | "Here's what I know about you and your work" |
| Control | Fully yours | You can ask Claude to correct or forget things |
| Scope | Often per-Project or per-skill | Account-wide, or separate per Project depending on its memory setting |

**Simple analogy:** Instructions are a job description you hand a new employee. Memory is the employee's own notebook about you, built up over time. The employee follows the job description, and uses the notebook to avoid asking the same questions twice.

**Practical tips**
- For things you want enforced every time (format, tone, process), use instructions. Memory is not a guarantee.
- For background context (your role, current projects), memory is a good fit.
- If memory gets something wrong, tell Claude to correct or forget it. To turn memory off entirely, use the memory setting in Settings.

Want an example of when to use each for your own workflow?

## User (2026-10-12 10:35:35 EDT)

like i wanted to know, that where does this instruction go, because like llm take a peice of text only, but when user prompts, the instruction text gets added with prompts ? does this happens in the architecture of claude llm response?

## Claude (2026-10-12 10:35:35 EDT)

Yes, that's essentially what happens. You've understood the key point: **an LLM only ever sees one sequence of text (tokens).** There is no separate "instruction slot" inside the model.

**What actually happens when you send a message**

The app (claude.ai, the API, etc.) assembles everything into one long input before the model sees it:

```
[ System prompt: Anthropic's built-in rules, tool descriptions, date, etc. ]
[ Your instructions: preferences, Project instructions, skills ]
[ Memory: saved notes about you ]
[ Earlier messages in this chat (yours + Claude's) ]
[ Your new message ]
        ↓
   Model reads all of this as tokens
        ↓
   Predicts the reply, one token at a time
```

The model then continues that text with its answer.

**Key points**

1. **The model is stateless.** It doesn't remember your last message on its own. On every turn, the app resends the entire conversation, plus the instructions and memory, all over again. The "memory" of the chat is just the history being pasted back in.

2. **Instructions and memory use the same mechanism.** Both are just text inserted into the input. The difference is not in the architecture but in *where the text comes from* (you wrote it vs. Claude saved it) and *how it's maintained*.

3. **Why instructions carry weight.** Text in the system or instruction position is formatted with special markers, and the model is *trained* to treat it as higher-authority guidance than ordinary chat text. So it's not "hardcoded" into the model. It's learned behavior, which is why it works very reliably but isn't a 100% guarantee.

4. **The model's weights don't change.** Neither instructions nor memory retrain the model. The weights (the billions of learned numbers) are fixed after training. Everything you add only changes the *input*.

5. **Context window limit.** The model can read only a limited amount of text at once. Instructions, memory, history, and attached files all compete for that space, which is why very long chats eventually need trimming or summarizing, and why memory stores short notes rather than full transcripts.

**One-line summary:** instructions and memory are both pieces of text that the app prepends to your message every single time. The model reads the whole bundle as one prompt and writes the continuation.

If you want to go deeper, the next concepts to look at are **system prompts vs. user prompts** (roles), **context windows**, and **tokens**.

## User (2026-10-12 10:35:35 EDT)

like can you  show me the example what text goes in when we add instruction with prompt, and memory ,   and what do you mean by instruction weights more than prompt and memoery ?

## Claude (2026-10-12 10:35:35 EDT)

Here's a simplified example. The real format is more complex (special tokens, structured roles), but the idea is the same.

**What the model receives (illustrative)**

```
SYSTEM:
You are Claude, made by Anthropic. Today's date is 9 Oct 2026.
You can use these tools: web search, file creation...
Follow safety guidelines...

USER INSTRUCTIONS (set by you):
Always answer in bullet points. Keep answers under 100 words.

MEMORY (saved notes about you):
- Works as an intern on an AI testing team
- Prefers simple explanations with analogies

CONVERSATION SO FAR:
User: What is photosynthesis?
Claude: [earlier reply]

User: Explain how chlorophyll works.   <-- your new prompt
```

The model reads all of this top to bottom and writes the next reply. Using the instructions and memory above, it would probably answer in short bullets, with a simple analogy.

**What "instructions carry more weight" means**

I should be careful with the word "weight," because it has two meanings:

- **Model weights** are the billions of fixed numbers learned in training. Instructions do *not* change these.
- **Priority or authority** is what I meant. During training, the model learns that text in certain positions should be treated as more binding than others.

So it's a learned habit, not a technical rule. Roughly:

1. **System-level rules** (safety, built-in behavior) rank highest.
2. **Your instructions** are standing orders: "always do X."
3. **Your current prompt** is the specific request right now.
4. **Memory** is background context. It informs the answer but doesn't command it.

**Why memory ranks lower:** memory is Claude's own notes, which could be outdated or wrong. Instructions are something you deliberately wrote, so they're treated as more reliable.

**Conflict examples**

| Situation | What usually happens |
|---|---|
| Instruction says "bullets", memory says "likes paragraphs" | Bullets win. The instruction is explicit, the memory is a softer hint. |
| Instruction says "bullets", but your prompt says "explain in a paragraph this time" | Usually the paragraph wins. You wrote both, and the specific, recent request reflects your current intent. |
| Memory says "likes analogies", but your prompt is "just give me the code" | Memory is skipped. It's only used when it helps the current question. |
| Any text tells Claude to ignore safety rules | Refused. System-level rules sit above everything. |

This is a tendency, not a strict ladder. The model weighs authority, how specific the text is, and what you most plausibly want, so it's very reliable but not mathematically guaranteed. That's why important rules are best stated clearly in instructions rather than left to memory.
