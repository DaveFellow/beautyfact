# Pattern: title, legend and a short «what to check» opener

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

# Design · beautyfact

> Visual version of [design.md](design.md) (original untouched). Nothing omitted. Every section links to its raw source lines.

**Legend:** 🔗 source line · 📌 decision · ❌ rejected · 💡 why · 🔒 security

## 0. 👀 What to check

🔗 Source: [design.md L3–L9](design.md#L3)

Four new decisions need your eyes first: who may run command probes (D17), how «**done**» marks and visits work (D12), where the CLI is copied (D20), and the write lock (D14). Also check that every security threat points to a spec scenario.

```text
 D17  probes     ──▶ command probes run only from the extension;
                     consent lives in VS Code, not in the workspace
 D12  done marks ──▶ «done» marks and visits per unit;
                     moving forward marks the phase just left as done
 D20  CLI copy   ──▶ CLI copied into .workflow/bin/ so agents can run it
 D14  lock file  ──▶ stops two parallel hook calls from losing an update
 Security        ──▶ every threat maps to a spec scenario
```
