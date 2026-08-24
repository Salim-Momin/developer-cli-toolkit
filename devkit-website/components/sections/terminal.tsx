"use client";

import { useState, useRef } from "react";

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



const {

scrollYProgress

}=useScroll({

target:terminalRef,

offset:[
"start end",
"center center"
]

});



const progress =
useSpring(
scrollYProgress,
{

stiffness:90,

damping:25,

mass:.5

}
);





const scale =
useTransform(

progress,

[0,1],

[0.7,1]

);



const rotateX =
useTransform(

progress,

[0,1],

[35,0]

);



const translateY =
useTransform(

progress,

[0,1],

[160,0]

);



const opacity =
useTransform(

progress,

[0,1],

[0,1]

);





/*
Mouse camera
*/


const mouseX =
useMotionValue(0);


const mouseY =
useMotionValue(0);



const cameraX =
useSpring(

mouseX,

{
stiffness:120,
damping:20

}

);



const cameraY =
useSpring(

mouseY,

{
stiffness:120,
damping:20

}

);





function handleMouse(

e:React.MouseEvent<HTMLDivElement>

){


const box =
e.currentTarget.getBoundingClientRect();



const x =
(e.clientX-box.left)
/box.width;


const y =
(e.clientY-box.top)
/box.height;



mouseX.set(

(x-.5)*8

);


mouseY.set(

(y-.5)*-8

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




{/* Cinematic Glow */}


<motion.div


style={{

scale:useTransform(
progress,
[0,1],
[0.5,1.3]
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

rounded-full

bg-cyan-500/20

blur-[160px]

"

/>






<motion.div


onMouseMove={handleMouse}



style={{

scale,

rotateX,

y:translateY,

opacity,

rotateY:cameraX,

transformPerspective:1400

}}




whileHover={{

scale:1.04

}}




className="

relative

rounded-3xl

overflow-hidden

border

border-zinc-800

bg-[#050505]

shadow-[0_70px_150px_rgba(0,0,0,.8)]

"

>







{/* Terminal Header */}



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


<motion.span

animate={{
y:[0,-3,0]
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
y:[0,-3,0]
}}

transition={{
duration:2,
delay:.3,
repeat:Infinity
}}

className="
h-3
w-3
rounded-full
bg-yellow-400
"

/>



<motion.span

animate={{
y:[0,-3,0]
}}

transition={{
duration:2,
delay:.6,
repeat:Infinity
}}

className="
h-3
w-3
rounded-full
bg-green-400
"

/>



<span

className="
ml-3
text-xs
text-zinc-500
font-mono
"

>

devkit-terminal

</span>


</div>









{/* Terminal Screen */}



<div

className="
p-8
font-mono
"

>




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






<div

className="
mt-6
rounded-xl
border
border-zinc-800
bg-black/60
p-6
"

>


<TypeAnimation


sequence={[

output

]}


speed={15}


cursor={true}


/>


</div>






</div>




</motion.div>



</section>

);

}