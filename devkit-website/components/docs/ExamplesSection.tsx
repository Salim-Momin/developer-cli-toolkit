"use client";

import { motion } from "framer-motion";


const examples = [

{
title:"Analyze a New Project",

icon:"📦",

description:
"Get complete information about any codebase instantly.",

steps:[

"devkit info",

"devkit stats",

"devkit tree"

],

result:
"Project structure, languages and files detected."

},


{
title:"Check Project Quality",

icon:"❤️",

description:
"Run health checks before deployment.",

steps:[

"devkit health",

"devkit doctor"

],

result:
"Health score and improvement suggestions generated."

},



{
title:"Debug Development Setup",

icon:"🩺",

description:
"Verify installed tools and environment configuration.",

steps:[

"devkit doctor"

],

result:
"Development environment diagnostics completed."

},



{
title:"Find Code Quickly",

icon:"🔎",

description:
"Search thousands of files using powerful filters.",

steps:[

`devkit search "import"`,

`devkit search "TODO"`

],

result:
"Relevant code matches displayed instantly."

},



{
title:"Manage Git Repository",

icon:"🌿",

description:
"Inspect repository status without leaving terminal.",

steps:[

"devkit git status",

"devkit git branches"

],

result:
"Repository state and history available."

},


];




export default function ExamplesSection(){



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


{/* Header */}


<motion.div

initial={{

opacity:0,

y:30

}}

whileInView={{

opacity:1,

y:0

}}

viewport={{

once:true

}}

className="
text-center
"

>


<p

className="
font-mono
text-sm
tracking-widest
text-cyan-400
"

>

EXAMPLES

</p>



<h2

className="
mt-5
text-4xl
font-bold
text-white
md:text-6xl
"

>

Developer Workflows

</h2>



<p

className="
mx-auto
mt-5
max-w-xl
text-zinc-400
"

>

Real examples showing how DevKit
helps developers work faster.

</p>



</motion.div>







{/* Cards */}


<div

className="
mt-16
grid
gap-8
md:grid-cols-2
"

>


{

examples.map((example,index)=>(



<motion.div


key={example.title}



initial={{

opacity:0,

y:60

}}



whileInView={{

opacity:1,

y:0

}}



viewport={{

once:true

}}



transition={{

duration:.7,

delay:index*.1

}}



whileHover={{

y:-8

}}



className="
group
rounded-2xl
border
border-zinc-800
bg-black/40
p-8
backdrop-blur
transition
"

>


<div

className="
text-4xl
"

>

{example.icon}

</div>



<h3

className="
mt-5
text-xl
font-semibold
text-white
"

>

{example.title}

</h3>




<p

className="
mt-3
text-zinc-400
"

>

{example.description}

</p>





{/* Terminal */}

<div

className="
mt-6
rounded-xl
border
border-zinc-800
bg-[#050505]
p-5
font-mono
text-sm
"

>


{

example.steps.map((step)=>(


<p

key={step}

className="
text-cyan-300
"

>

$ {step}

</p>


))


}



</div>





<p

className="
mt-5
text-sm
text-green-400
"

>

✓ {example.result}

</p>





</motion.div>



))


}



</div>



</section>

);

}