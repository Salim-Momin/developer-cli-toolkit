"use client";
import { motion } from "framer-motion";

import FeatureCard from "./FeatureCard";
import FeatureParticles from "./FeatureParticles";

const features = [
  {
    title: "Project Information",
    description:
      "Inspect any project instantly with a complete overview including language, project size, repository status, files, directories and development environment.",
    icon: "📦",
    type: "project-info",
    points: [
      "Project overview",
      "Language detection",
      "Project size",
      "Git repository",
    ],
  },

  {
    title: "Project Statistics",
    description:
      "Visualize your project composition with language statistics, extension breakdowns and detailed file analytics.",
    icon: "📊",
    type: "project-stats",
    points: [
      "Language statistics",
      "Extension breakdown",
      "File analytics",
      "Project metrics",
    ],
  },

  {
    title: "Project Health",
    description:
      "Automatically validate your project structure and receive health reports with recommendations to improve code quality.",
    icon: "❤️",
    type: "project-health",
    points: [
      "Health score",
      "Configuration checks",
      "Project diagnostics",
      "Recommendations",
    ],
  },

  {
    title: "Project Tree",
    description:
      "Browse your complete project structure directly from the terminal with a clean tree view and folder hierarchy.",
    icon: "🌳",
    type: "project-tree",
    points: [
      "Directory tree",
      "Folder hierarchy",
      "Project structure",
      "Tree summary",
    ],
  },

  {
    title: "Smart Search",
    description:
      "Search across your entire project using text search, filename search, regex support and extension filtering.",
    icon: "🔎",
    type: "search",
    points: [
      "Text search",
      "Filename search",
      "Regex support",
      "Extension filters",
    ],
  },

  {
    title: "Environment Doctor",
    description:
      "Analyze your development environment and verify installed tools, versions and configuration before you start coding.",
    icon: "🩺",
    type: "doctor",
    points: [
      "Tool detection",
      "Environment diagnostics",
      "Version checks",
      "Recommendations",
    ],
  },

  {
    title: "Git Toolkit",
    description:
      "Inspect repository status, branches, remotes, synchronization and commit history without leaving the terminal.",
    icon: "🌿",
    type: "git",
    points: [
      "Repository status",
      "Branch management",
      "Commit history",
      "Git health",
    ],
  },

  {
    title: "API Tester",
    description:
      "Send HTTP requests directly from DevKit with support for GET, POST, PUT, PATCH and DELETE methods.",
    icon: "🌐",
    type: "api",
    points: [
      "GET requests",
      "POST requests",
      "PUT / PATCH",
      "DELETE requests",
    ],
  },
];

export default function FeatureSection(){


return (

<section
id="features"

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