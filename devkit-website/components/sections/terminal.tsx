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
██████╗ ███████╗██╗   ██ ╗██╗  ██╗██╗████████╗
██╔══██╗██╔════╝██║   ██ ║██║ ██╔╝██║╚══██╔══╝
██║  ██║█████╗  ██║   ██ ║█████╔╝ ██║   ██║
██║  ██║██╔══╝  ╚██╗ ██╔ ╝██╔═██╗ ██║   ██║
██████╔╝███████╗ ╚████╔╝  ██║  ██╗██║   ██║
╚═════╝ ╚══════╝  ╚═══╝   ╚═╝  ╚═╝╚═╝   ╚═╝
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
mass:.3
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
[80,0]
);



const scrollRotate =
useTransform(
smooth,
[0,1],
[25,0]
);



const opacity =
useTransform(
smooth,
[0,1],
[0,1]
);




const mouseX =
useMotionValue(0);

const mouseY =
useMotionValue(0);



const rotateY =
useSpring(mouseX,{
stiffness:150,
damping:20
});



const rotateX =
useSpring(mouseY,{
stiffness:150,
damping:20
});



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
(x-box.width/2)/15
);



mouseY.set(
-(y-box.height/2)/15
);


}



return (

<section
id="terminal"

ref={terminalRef}

className="
relative
overflow-hidden
py-32
"

>


{/* OUTSIDE BACKGROUND */}


<div className="
absolute
inset-0
">


{/* Radial */}

<div

className="
absolute
inset-0
bg-[radial-gradient(circle_at_top,#06b6d420,transparent_60%)]
"

/>



{/* Animated Grid */}

<motion.div

animate={{

backgroundPosition:[
"0px 0px",
"64px 64px"
]

}}

transition={{

duration:12,
repeat:Infinity,
ease:"linear"

}}

className="
absolute
inset-0
bg-[linear-gradient(rgba(255,255,255,.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.02)_1px,transparent_1px)]
bg-[size:64px_64px]
"

/>




{/* Cyan Orb */}

<motion.div

animate={{

x:[
-40,
40,
-40
],

y:[
0,
-40,
0

]

}}

transition={{

duration:12,
repeat:Infinity,
ease:"easeInOut"

}}

className="
absolute
left-20
top-20
h-96
w-96
rounded-full
bg-cyan-500/10
blur-[160px]
"

/>




{/* Blue Orb */}

<motion.div

animate={{

x:[
40,
-40,
40
],

y:[
0,
50,
0

]

}}

transition={{

duration:15,
repeat:Infinity,
ease:"easeInOut"

}}

className="
absolute
right-0
bottom-0
h-[500px]
w-[500px]
rounded-full
bg-blue-500/10
blur-[180px]
"

/>



</div>






{/* Glow Behind Window */}


<motion.div

style={{

scale:useTransform(
smooth,
[0,1],
[.5,1.4]
)

}}

className="
absolute
left-1/2
top-1/2
-translate-x-1/2
-translate-y-1/2
h-[500px]
w-[700px]
rounded-full
bg-cyan-500/20
blur-[160px]
"

/>





<div

className="
relative
z-10
mx-auto
max-w-6xl
px-6
"

>



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


{/* HEADER */}

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


<span className="h-3 w-3 rounded-full bg-red-500 animate-pulse"/>

<span className="h-3 w-3 rounded-full bg-yellow-400 animate-pulse"/>

<span className="h-3 w-3 rounded-full bg-green-400 animate-pulse"/>


<span className="
ml-3
text-xs
font-mono
text-zinc-500
">

devkit-terminal

</span>


</div>





{/* SCREEN */}

<div

className="
relative
overflow-hidden
p-8
font-mono
"

>


{/* INNER GRID */}

<div

className="
absolute
inset-0
bg-[linear-gradient(rgba(6,182,212,.05)_1px,transparent_1px),linear-gradient(90deg,rgba(6,182,212,.05)_1px,transparent_1px)]
bg-[size:48px_48px]
"

/>



<div

className="
absolute
inset-0
bg-cyan-500/10
blur-[120px]
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


</div>

{/* Section Bottom Merge Glow */}

<div

className="
pointer-events-none
absolute
bottom-0
left-1/2
-translate-x-1/2
h-32
w-[80%]
rounded-full
bg-cyan-500/10
blur-[100px]
"

/>

</section>

);

}