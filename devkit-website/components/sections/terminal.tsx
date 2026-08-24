"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { TypeAnimation } from "react-type-animation";
import { Terminal } from "lucide-react";


const commands = {

"project info":
`
Project:
Developer CLI Toolkit

Language:
Python

Files:
124

Health:
98/100
`,

"git health":
`
Repository:
developer-cli-toolkit

Branch:
main

Changes:
Clean

Health:
100%
`,

"doctor":
`
Environment Check

✓ Python installed
✓ Git installed
✓ Node installed

System:
Healthy
`,

"api get":
`
HTTP Request

Status:
200 OK

Response:
Success
`

};



const commandList = Object.keys(commands);



export default function TerminalPlayground(){


const [output,setOutput] = useState(
"Waiting for command..."
);


return (

<section
id="terminal"

className="
py-32
max-w-6xl
mx-auto
px-6
"
>


{/* Section Title */}

<motion.div

initial={{
opacity:0,
y:40
}}

whileInView={{
opacity:1,
y:0
}}

viewport={{
once:true,
amount:0.3
}}

transition={{
duration:0.7
}}

className="
mb-14
"

>


<p
className="
font-mono
text-sm
text-zinc-500
"
>

02 / TERMINAL

</p>


<h2
className="
mt-4
text-4xl
md:text-5xl
font-semibold
text-white
"

>

Experience DevKit

inside your browser.

</h2>


<p
className="
mt-4
text-zinc-400
max-w-xl
"
>

A simulated terminal environment
showing how DevKit works.

</p>


</motion.div>





{/* Terminal Window */}


<motion.div

initial={{
opacity:0,
y:80,
scale:0.95
}}

whileInView={{
opacity:1,
y:0,
scale:1
}}

viewport={{
once:true,
amount:0.2
}}

transition={{
duration:0.8,
ease:"easeOut"
}}


className="
rounded-2xl
border
border-zinc-800
bg-[#0D0D0D]
overflow-hidden
shadow-2xl
"

>


{/* Terminal Header */}

<div

className="
flex
items-center
gap-3
px-5
py-4
border-b
border-zinc-800
"

>


<motion.span

animate={{
opacity:[1,0.4,1]
}}

transition={{
duration:2,
repeat:Infinity
}}

className="
h-3
w-3
rounded-full
bg-red-500
"

/>


<motion.span

animate={{
opacity:[1,0.4,1]
}}

transition={{
duration:2,
delay:0.3,
repeat:Infinity
}}

className="
h-3
w-3
rounded-full
bg-yellow-500
"

/>


<motion.span

animate={{
opacity:[1,0.4,1]
}}

transition={{
duration:2,
delay:0.6,
repeat:Infinity
}}

className="
h-3
w-3
rounded-full
bg-green-500
"

/>



<span
className="
ml-3
font-mono
text-xs
text-zinc-500
"
>

devkit-terminal

</span>


</div>





{/* Terminal Body */}


<div

className="
p-6
font-mono
"

>


{/* Command Buttons */}


<div
className="
flex
flex-wrap
gap-3
mb-10
"

>


{

commandList.map((command,index)=>(


<motion.button

key={command}

initial={{
opacity:0,
y:20
}}

whileInView={{
opacity:1,
y:0
}}

viewport={{
once:true
}}

transition={{
delay:index*0.15
}}


whileHover={{
scale:1.05
}}


onClick={()=>setOutput(commands[command as keyof typeof commands])}


className="
border
border-zinc-800
rounded-lg
px-4
py-2
text-sm
text-zinc-400
hover:text-cyan-400
hover:border-cyan-400
transition
"

>

$ devkit {command}

</motion.button>


))

}


</div>





{/* Terminal Output */}


<div

className="
rounded-lg
bg-black
border
border-zinc-900
p-5
min-h-[220px]
"

>


<div
className="
text-green-400
mb-4
"

>

$ devkit execute

<span
className="
animate-pulse
"
>
_
</span>

</div>



<TypeAnimation

key={output}

sequence={[

output,
5000

]}

speed={35}

cursor={false}

/>


</div>



</div>


</motion.div>



</section>


)

}