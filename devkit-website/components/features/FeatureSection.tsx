"use client";

import { useState } from "react";
import { motion } from "framer-motion";

import FeatureCard from "./FeatureCard";
import FeatureParticles from "./FeatureParticles";
import FeatureIndicator from "./FeatureIndicator";


const features = [

  {
    title: "Project Analyzer",

    description:
      "Deeply analyze your codebase, detect project structure, frameworks, dependencies and overall project health directly from your terminal.",

    icon: "🔍",

    type: "project",

    points: [
      "Framework detection",
      "Project statistics",
      "File structure analysis",
      "Project health report",
    ],
  },


  {
    title: "Git Toolkit",

    description:
      "Manage repositories faster with powerful Git utilities for status checking, branches, history and repository health.",

    icon: "🌿",

    type: "git",

    points: [
      "Repository status",
      "Branch tracking",
      "Commit history",
      "Git health monitoring",
    ],
  },


  {
    title: "Smart Search",

    description:
      "Search your entire project instantly with developer-focused filtering, regex support and fast results.",

    icon: "🔎",

    type: "search",

    points: [
      "Code searching",
      "Regex support",
      "File filtering",
      "Fast results",
    ],
  },


  {
    title: "API Tester",

    description:
      "Test APIs directly from your terminal with request handling, response inspection and debugging tools.",

    icon: "🌐",

    type: "api",

    points: [
      "HTTP requests",
      "JSON handling",
      "Header support",
      "Response analysis",
    ],
  },

];





export default function FeatureSection(){


const [active,setActive] = useState(0);



return (

<section

className="
relative
overflow-hidden
py-32
"

>


{/* Background */}

<div className="absolute inset-0">


<div

className="
absolute
inset-0
bg-[radial-gradient(circle_at_top,#06b6d420,transparent_60%)]
"

/>



<div

className="
absolute
inset-0
bg-[linear-gradient(rgba(255,255,255,.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.02)_1px,transparent_1px)]
bg-[size:64px_64px]
"

/>



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




{/* Floating particles */}


<FeatureParticles />



{/* Active navigation */}

<FeatureIndicator

active={active}

/>




<div

className="
relative
mx-auto
max-w-7xl
px-6
"

>



{/* Heading */}


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

once:true

}}


transition={{

duration:.8

}}


className="
mx-auto
max-w-3xl
text-center
"


>


<p

className="
mb-4
font-mono
text-sm
tracking-widest
text-cyan-400
"

>

FEATURES

</p>



<h2

className="
text-4xl
font-bold
tracking-tight
text-white
md:text-6xl
"

>

Powerful Tools.

<br />

Built For Developers.

</h2>



<p

className="
mt-6
text-lg
leading-relaxed
text-zinc-400
"

>

Everything developers need to
build, debug and automate
from one powerful terminal.

</p>



</motion.div>







{/* Feature Cards */}


<div

className="
mt-28
space-y-40
"

>


{

features.map((feature,index)=>(


<motion.div


key={feature.title}



onViewportEnter={()=>setActive(index)}



viewport={{

amount:.5

}}



initial={{

opacity:0,

y:80

}}



whileInView={{

opacity:1,

y:0

}}



transition={{

duration:.9,

delay:index*.1

}}



>



<FeatureCard


title={feature.title}

description={feature.description}

icon={feature.icon}

type={feature.type}

points={feature.points}

reverse={index % 2 !== 0}



/>



</motion.div>



))


}



</div>



</div>



</section>

);

}