"use client";

import { motion } from "framer-motion";
import { TypeAnimation } from "react-type-animation";


type Props = {
  type: string;
};


const outputs = {

  project: `
$ devkit project info

Analyzing project...

✓ Framework detected
✓ TypeScript enabled
✓ Components found: 48
✓ Files scanned: 324

Project health: Excellent
`,

  git: `
$ devkit git health

Checking repository...

✓ Branch: main
✓ Clean working tree
✓ Remote connected
✓ Latest commit synced

Git status: Healthy
`,

  search: `
$ devkit search "TODO"

Searching source files...

18 matches found

src/app/page.tsx
src/components/navbar.tsx
src/hooks/useAuth.ts

Search completed ✓
`,

  api: `
$ devkit api get /users

Sending request...

Status: 200 OK

Response time:
245ms

{
 success:true
}

`,
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

text,

]}

speed={35}

cursor={true}

/>


</div>



</motion.div>

);

}