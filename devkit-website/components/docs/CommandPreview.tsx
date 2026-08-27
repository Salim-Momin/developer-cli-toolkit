"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Copy, Check } from "lucide-react";


const commands = [

{
command:"devkit info",

title:"Project Information",

description:
"Display complete project overview including files, language, size and repository information.",

output:
`
📦 Project Information

developer-cli-toolkit


Project Overview

Name              developer-cli-toolkit
Language          Python
Size              833.89 KB
Files             99
Directories       21

README            ✓ Yes
Git Repository    ✓ Yes
`
},


{
command:"devkit stats",

title:"Project Statistics",

description:
"Analyze project composition with language and extension statistics.",

output:
`
📊 Project Statistics


Language Statistics

Python            41
TypeScript        15
Markdown           8
JSON               5
CSS                1
YAML               1


Top Extensions

.py               41
.tsx              13
.md                8
.json              5
`
},


{
command:"devkit health",

title:"Project Health",

description:
"Check project quality and get recommendations.",

output:
`
❤️ Project Health


███████████████████░░░░░

Health Score

80 / 100


README          ● PASS
Tests           ● PASS
Docker          ● WARN
Git             ● PASS


Recommendations

• Add .env.example
`
},


{
command:"devkit tree",

title:"Project Tree",

description:
"Explore complete project structure.",

output:
`
🌳 Project Tree


📦 developer-cli-toolkit

├── src
├── tests
├── docs
├── devkit-website
├── README.md
├── pyproject.toml


Summary

10 directories
35 files
`
},


{
command:'devkit search "import"',

title:"Smart Search",

description:
"Search your codebase instantly.",

output:
`
🔎 Smart Search


Searching:

"import"


225 matches found


eslint.config.mjs

Line 1

import { defineConfig }


Showing 5 of 225 matches
`
},


{
command:"devkit doctor",

title:"Environment Doctor",

description:
"Inspect installed developer tools.",

output:
`
🩺 Environment Doctor


Python       ✓ PASS
Node.js      ✓ PASS
Git          ✓ PASS
Docker       ✓ PASS
Java         ✓ PASS
VS Code      ✓ PASS


Health Score

90 / 100
`
},


{
command:"devkit git status",

title:"Git Toolkit",

description:
"Inspect repository status.",

output:
`
🌿 Git Status


Branch

main


Modified     0
Staged       0
Deleted      0


✓ Working tree is clean.
`
}

];




export default function CommandPreview(){


const [active,setActive] = useState(0);

const [copied,setCopied] = useState(false);



function copyCommand(){

navigator.clipboard.writeText(
commands[active].command
);


setCopied(true);


setTimeout(()=>{

setCopied(false);

},1500);

}




return (

<section

className="
relative
mx-auto
mt-32
max-w-6xl
px-6
"

>


<div

className="
grid
gap-10
md:grid-cols-2
"

>


{/* Command List */}


<div

className="
space-y-3
"

>


{

commands.map((item,index)=>(


<button


key={item.command}


onClick={()=>setActive(index)}


className={`
w-full
rounded-xl
border
p-5
text-left
transition

${

active===index

?

"border-cyan-500 bg-cyan-500/10"

:

"border-zinc-800 bg-black/30"

}

`}


>


<p

className="
font-mono
text-cyan-400
"

>

$

{item.command}

</p>



<p

className="
mt-2
text-sm
text-zinc-400
"

>

{item.title}

</p>



</button>


))


}


</div>





{/* Terminal */}


<motion.div

layout

className="
overflow-hidden
rounded-2xl
border
border-zinc-800
bg-[#050505]
shadow-2xl
"

>


{/* Header */}

<div

className="
flex
items-center
justify-between
border-b
border-zinc-800
px-5
py-4
"

>


<div className="flex gap-2">


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
bg-yellow-500
"/>


<span className="
h-3
w-3
rounded-full
bg-green-500
"/>


</div>



<button

onClick={copyCommand}

className="
flex
items-center
gap-2
text-sm
text-zinc-400
hover:text-white
"

>

{

copied ?

<Check size={16}/>

:

<Copy size={16}/>

}


{

copied ?

"Copied"

:

"Copy"

}

</button>



</div>





<div

className="
p-6
font-mono
text-sm
leading-7
text-zinc-300
"

>


<AnimatePresence mode="wait">


<motion.pre

key={active}


initial={{

opacity:0,

y:20

}}


animate={{

opacity:1,

y:0

}}


exit={{

opacity:0,

y:-20

}}


transition={{

duration:.3

}}


>

{commands[active].output}


</motion.pre>


</AnimatePresence>



</div>


</motion.div>


</div>


</section>


);

}