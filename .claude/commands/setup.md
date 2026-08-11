---
description: Set up the business identity and working rules in CLAUDE.md through a guided conversation.
disable-model-invocation: true
---

# Set up this business brain

Read `CLAUDE.md` before replying. Find every bracketed prompt in that file, then help the user replace each one with a clear answer.

## Conversation rules

1. Ask one question at a time.
2. Use friendly, everyday language. Give a short example when a prompt may be unfamiliar.
3. Start with the business name, then cover what the business does and who it serves.
4. Ask about tone with customers or clients and tone with the team separately.
5. Gather the always list, the never list, and the hard rules one item at a time.
6. Skip any prompt that already has a real answer. Offer to revise it only when it conflicts with a later answer.
7. If the user doesn't know an answer, record `Not set yet` instead of guessing.

Keep the privacy rules and the instructions about reading the knowledge base and asking instead of guessing. Don't weaken or remove them.

After the last answer, write the completed `CLAUDE.md`. Preserve its headings and useful instructions. Check that no bracketed prompts remain, except brackets the user asked to keep as normal text.

End with one useful next step:

- If the user has existing material, ask them to put two or three files in `_inbox/` and run `/ingest`.
- If nothing is written down yet, suggest `/interview`.
