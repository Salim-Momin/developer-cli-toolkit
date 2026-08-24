"use client";

import { useRef } from "react";

import {
  motion,
  useScroll,
  useTransform,
  useSpring,
  useMotionValue,
} from "framer-motion";

import { TypeAnimation } from "react-type-animation";


const banner = `
██████╗ ███████╗██╗   ██╗██╗  ██╗██╗████████╗
██╔══██╗██╔════╝██║   ██║██║ ██╔╝██║╚══██╔══╝
██║  ██║█████╗  ██║   ██║█████╔╝ ██║   ██║
██║  ██║██╔══╝  ╚██╗ ██╔╝██╔═██╗ ██║   ██║
██████╔╝███████╗ ╚████╔╝ ██║  ██╗██║   ██║
╚═════╝ ╚══════╝  ╚═══╝  ╚═╝  ╚═╝╚═╝   ╚═╝
`;


const output = `
Developer CLI Toolkit

Build • Debug • Analyze • Automate


DevKit v0.1.0


PROJECT

1       🔍 Project Information
2       📊 Project Statistics
3       ❤️ Project Health
4       🌳 Project Tree


DEVELOPER TOOLS

5       🔎 Smart Search
6       🩺 Environment Doctor
7       🌿 Git Toolkit
8       🌐 API Tester


9       🤖 AI Assistant

10      📚 Command Reference


0       ❌ Exit


Enter number · h for help · q to quit


Choose a command [0]:
`;



export default function Terminal(){

const terminalRef =
useRef<HTMLDivElement>(null);



/*
Scroll camera animation
*/

const {
scrollYProgress
}=useScroll({

target:terminalRef,

offset:[
"start end",
"center center"
]

});



const smooth =
useSpring(
scrollYProgress,
{
stiffness:140,
damping:20,
mass:0.3
}
);

const scale =
useTransform(
smooth,
[0,1],
[0.85,1]
);


const translateY =
useTransform(
smooth,
[0,1],
[70,0]
);



const scrollRotate =
useTransform(
smooth,
[0,1],
[30,0]
);

const opacity =
useTransform(
smooth,
[0,1],
[0,1]
);





/*
Mouse camera movement
*/


const mouseX =
useMotionValue(0);

const mouseY =
useMotionValue(0);


const rotateY =
useSpring(
mouseX,
{
stiffness:150,
damping:20,
mass:0.4
}
);


const rotateX =
useSpring(
mouseY,
{
stiffness:150,
damping:20,
mass:0.4
}
);


function handleMouse(
e:React.MouseEvent<HTMLDivElement>
){

const box =
e.currentTarget.getBoundingClientRect();


const x =
e.clientX-box.left;

const y =
e.clientY-box.top;


mouseX.set(
(x-box.width/2)/18
);


mouseY.set(
-(y-box.height/2)/18
);

}



return (

<section

ref={terminalRef}

className="
relative
py-32
max-w-6xl
mx-auto
px-6
"

>


{/* Background Glow */}

<motion.div

style={{

scale:useTransform(
smooth,
[0,1],
[0.5,1.4]
)

}}

className="
absolute
left-1/2
top-1/2
-translate-x-1/2
-translate-y-1/2

w-[600px]
h-[400px]

bg-cyan-500/20

blur-[150px]

rounded-full

"

/>





<div
style={{
perspective:1400
}}
>


<motion.div


onMouseMove={handleMouse}


style={{

scale,

y:translateY,

opacity,


rotateX,


rotateY,


transformPerspective:1400

}}


whileHover={{

scale:1.03

}}



className="

relative

rounded-3xl

overflow-hidden

border

border-zinc-800

bg-[#050505]

shadow-[0_70px_150px_rgba(0,0,0,.85)]

"

>



{/* Header */}


<div

className="
flex
items-center
gap-3
px-6
py-4
border-b
border-zinc-800
"

>


<span className="
h-3
w-3
rounded-full
bg-red-500
animate-pulse
"/>


<span className="
h-3
w-3
rounded-full
bg-yellow-400
animate-pulse
"/>


<span className="
h-3
w-3
rounded-full
bg-green-400
animate-pulse
"/>


<span className="
ml-3
text-xs
text-zinc-500
font-mono
">

devkit-terminal

</span>


</div>






{/* Screen */}


<div

className="
relative
overflow-hidden
p-8
font-mono
"

>


{/* Scanlines */}

<motion.div

animate={{
y:[
"-100%",
"100%"
]
}}

transition={{

duration:8,

repeat:Infinity,

ease:"linear"

}}

className="

absolute

inset-0

z-20

pointer-events-none

opacity-[0.07]

bg-[linear-gradient(
transparent_50%,
cyan_50%
)]

bg-[length:100%_5px]

"

/>



{/* Reflection */}

<motion.div

animate={{

x:[
"-120%",
"120%"
]

}}

transition={{

duration:5,

repeat:Infinity,

ease:"linear"

}}

className="

absolute

top-0

left-0

h-full

w-1/3

z-30

pointer-events-none

bg-gradient-to-r

from-transparent

via-white/10

to-transparent

skew-x-12

"

/>





<div className="
relative
z-10
">


<pre

className="
text-cyan-400
text-[10px]
md:text-sm
leading-tight
"

>

{banner}

</pre>





<motion.div


animate={{

boxShadow:[

"0 0 0px transparent",

"0 0 35px rgba(0,255,255,.3)",

"0 0 0px transparent"

]

}}

transition={{

duration:3,

repeat:Infinity

}}


className="

mt-8

rounded-xl

border

border-cyan-900

bg-black/70

p-6

text-zinc-300

"

>



<TypeAnimation


sequence={[

"Initializing DevKit...\n\n",

1000,

"Loading Project Analyzer...\n",

700,

"Loading Git Engine...\n",

700,

"Loading API Tester...\n",

700,

"Environment Check Complete ✓\n\n",

800,

output

]}


speed={18}


cursor


/>


</motion.div>



</div>



</div>




</motion.div>

</div>


</section>

);

}