"use client";

import { motion } from "framer-motion";
import { Search } from "lucide-react";
import DocsCards from "@/components/docs/DocsCards";
import CommandPreview from "@/components/docs/CommandPreview";
import InstallationGuide from "@/components/docs/InstallationGuide";
import ExamplesSection from "@/components/docs/ExamplesSection";
import DocsFooter from "@/components/docs/DocsFooter";

export default function DocsPage(){

return (

<main

className="
relative
min-h-screen
overflow-hidden
bg-[#09090B]
px-6
pt-32
pb-20
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
-30,
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





{/* Content */}


<section

className="
relative
mx-auto
max-w-5xl
text-center
"

>


<motion.p

initial={{
opacity:0,
y:20
}}

animate={{
opacity:1,
y:0
}}

className="
font-mono
text-sm
tracking-widest
text-cyan-400
"

>

DOCUMENTATION

</motion.p>





<motion.h1

initial={{
opacity:0,
y:30
}}

animate={{
opacity:1,
y:0
}}

transition={{
delay:.1
}}

className="
mt-6
text-5xl
font-semibold
tracking-tight
text-white
md:text-7xl
"

>

Everything you need

<br/>

to master DevKit.

</motion.h1>





<motion.p

initial={{
opacity:0
}}

animate={{
opacity:1
}}

transition={{
delay:.3
}}

className="
mx-auto
mt-6
max-w-2xl
text-lg
text-zinc-400
"

>

Learn commands, workflows and developer
tools available inside the DevKit terminal.

</motion.p>





{/* Search */}
<DocsCards />

<CommandPreview />

<InstallationGuide />

<ExamplesSection />

<DocsFooter />

</section>

</main>

);

}