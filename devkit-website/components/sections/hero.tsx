"use client";

import { motion } from "framer-motion";
import { Terminal } from "lucide-react";
import { FaGithub } from "react-icons/fa";


export default function Hero() {


return (

<section
id="home"
className="
relative
overflow-hidden
min-h-screen
flex
items-center
justify-center
px-6
pt-24
"
>

{/* Background */}

<div className="absolute inset-0">

  {/* Radial Cyan Glow */}

  <div
  className="
  absolute
  inset-0
  bg-[radial-gradient(circle_at_top,#06b6d420,transparent_60%)]
  "
  />


  {/* Grid */}

  <div
  className="
  absolute
  inset-0
  bg-[linear-gradient(rgba(255,255,255,.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.02)_1px,transparent_1px)]
  bg-[size:64px_64px]
  "
  />


  {/* Cyan Floating Glow */}

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
  top-10
  h-96
  w-96
  rounded-full
  bg-cyan-500/10
  blur-[160px]
  "

  />



  {/* Blue Floating Glow */}

  <motion.div

  animate={{
    x:[
      30,
      -30,
      30
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

{/* HERO CONTENT */}


<div

className="
relative
z-10
mx-auto
w-full
max-w-5xl
text-center
"

>



{/* badge */}



<motion.div


initial={{

opacity:0,

y:20

}}


animate={{

opacity:1,

y:0

}}


transition={{

duration:.6

}}


className="
inline-flex
items-center
gap-2
rounded-full
border
border-zinc-800
bg-black/40
px-4
py-2
text-sm
text-zinc-400
backdrop-blur
"

>


<Terminal size={15}/>


Developer CLI Toolkit


</motion.div>







{/* Heading */}


<motion.h1


initial={{

opacity:0,

y:40

}}


animate={{

opacity:1,

y:0

}}


transition={{

duration:.8,

delay:.1

}}


className="
mt-8
text-5xl
font-semibold
tracking-tight
text-white
md:text-7xl
"

>


Powerful tools.


<br/>


Inside your


<span

className="
text-zinc-500
"

>

terminal.

</span>



</motion.h1>








{/* Description */}



<motion.p


initial={{

opacity:0

}}


animate={{

opacity:1

}}


transition={{

duration:.8,

delay:.3

}}



className="
mx-auto
mt-6
max-w-2xl
text-lg
leading-relaxed
text-zinc-400
"

>


Analyze projects, manage Git,
test APIs and automate developer
workflows without leaving your command line.



</motion.p>








{/* Buttons */}



<motion.div


initial={{

opacity:0,

y:20

}}


animate={{

opacity:1,

y:0

}}


transition={{

duration:.8,

delay:.5

}}


className="
mt-10
flex
justify-center
gap-4
"

>



<motion.button


whileHover={{

scale:1.05

}}


whileTap={{

scale:.95

}}



className="
rounded-xl
bg-white
px-6
py-3
text-sm
font-medium
text-black
transition
hover:bg-zinc-200
"

>


Install DevKit


</motion.button>







<motion.button


whileHover={{

scale:1.05

}}


whileTap={{

scale:.95

}}



className="
flex
items-center
gap-2
rounded-xl
border
border-zinc-800
bg-black/30
px-6
py-3
text-sm
text-white
backdrop-blur
transition
hover:bg-zinc-900
"

>


<FaGithub size={16}/>


GitHub


</motion.button>




</motion.div>







{/* Version */}



<motion.div


initial={{

opacity:0

}}


animate={{

opacity:1

}}


transition={{

delay:1

}}



className="
mt-16
font-mono
text-sm
text-zinc-600
"

>


DevKit v0.1.5


</motion.div>





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