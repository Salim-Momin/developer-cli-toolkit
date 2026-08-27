"use client";

import { motion } from "framer-motion";
import { TypeAnimation } from "react-type-animation";


type Props = {
  type: string;
};

const outputs: Record<string, string> = {

"project-info":`

📦 Project Information

developer-cli-toolkit


Project Overview

Name                 developer-cli-toolkit
Primary Language     Python
Project Size         833.89 KB
Files                99
Directories          21

README               ✓ Yes
.gitignore           ✓ Yes
Tests                ✓ Yes
Git Repository       ✓ Yes

`,



"project-stats":`

📊 Project Statistics

Language Statistics

Python               41
TypeScript           15
Markdown              8
JSON                  5
CSS                   1
YAML                  1


Top File Extensions

.py                  41
.tsx                 13
.md                   8
.json                 5
.png                  5
.svg                  5

`,



"project-health":`

❤️ Project Health

███████████████████░░░░░

Health Score

80 / 100


README               ● PASS
.gitignore           ● PASS
Tests                ● PASS
Environment          ● WARN
Docker               ● WARN
Git Repository       ● PASS


Recommendations

• Add a .env.example file

• Consider Docker support

`,



"project-tree":`

🌳 Project Tree

developer-cli-toolkit

├── src
├── tests
├── docs
├── devkit-website
├── README.md
├── pyproject.toml
├── requirements.txt
├── CHANGELOG.md

Summary

10 directories

35 files

`,



"search":`

🔎 Smart Search

Searching current project

Query

"import"


225 matches found


eslint.config.mjs

Line 1

import { defineConfig }

Showing 5 of 225 matches

`,



"doctor":`

🩺 Environment Doctor

Development Environment


Python          ✓ PASS

Node.js         ✓ PASS

Git             ✓ PASS

Docker          ✓ PASS

Java            ✓ PASS

PostgreSQL      ✓ PASS

VS Code         ✓ PASS

GitHub CLI      ⚠ WARN


Health Score

90 / 100


Recommendations

• Install GitHub CLI

• Start Docker daemon

`,



"git":`

🌿 Git Status

developer-cli-toolkit


Working Tree

Branch           main

Staged           0

Modified         0

Untracked        0

Deleted          0


✓ Working tree is clean.

`,



"api":`

🌐 API Tester

GET https://api.example.com/users


Status

200 OK


Response Time

245 ms


Content Type

application/json


✓ Request Successful

`

};
export default function FeatureTerminal({
  type,
}:Props){


const text =
outputs[type as keyof typeof outputs];



return (

<motion.div

whileHover={{
y:-8,
scale:1.02,
}}

transition={{
duration:.3,
}}

className="
group
relative
overflow-hidden
rounded-3xl
border
border-cyan-500/10
bg-black/70
shadow-[0_30px_80px_rgba(0,0,0,.7)]
"


>


{/* Glow */}

<div
className="
absolute inset-0
bg-cyan-500/5
opacity-0
transition
group-hover:opacity-100
"
/>



{/* Window Header */}

<div
className="
relative
flex
items-center
gap-3
border-b
border-zinc-800
px-6
py-4
"
>


<span className="
h-3
w-3
rounded-full
bg-red-500
"/>

<span className="
h-3
w-3
rounded-full
bg-yellow-400
"/>

<span className="
h-3
w-3
rounded-full
bg-green-400
"/>


<span className="
ml-3
font-mono
text-xs
text-zinc-500
">
devkit-terminal
</span>


</div>



{/* Screen */}

<div
className="
relative
min-h-[300px]
overflow-hidden
p-6
font-mono
text-sm
text-cyan-300
"
>


{/* Scanline */}

<motion.div

animate={{
y:["0%","100%"]
}}

transition={{
duration:6,
repeat:Infinity,
ease:"linear"
}}

className="
pointer-events-none
absolute
inset-0
opacity-[0.08]
bg-[linear-gradient(transparent_50%,rgba(0,255,255,.4)_50%)]
bg-[length:100%_6px]
"

/>



<TypeAnimation
  sequence={[
    "Initializing DevKit...\n\n",
    700,
    "Loading module...\n",
    500,
    outputs[type],
  ]}
  speed={35}
  cursor
/>


</div>



</motion.div>

);

}