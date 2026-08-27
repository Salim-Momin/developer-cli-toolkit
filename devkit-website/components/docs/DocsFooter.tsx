"use client";

import { motion } from "framer-motion";
import { FaGithub } from "react-icons/fa";
import { BookOpen } from "lucide-react";


export default function DocsFooter(){

return (

<footer

className="
relative
mt-40
overflow-hidden
border-t
border-zinc-800
py-24
"

>


{/* Glow */}

<div

className="
absolute
left-1/2
top-0
h-96
w-96
-translate-x-1/2
rounded-full
bg-cyan-500/10
blur-[160px]
"

/>



<div

className="
relative
mx-auto
max-w-5xl
px-6
text-center
"

>


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

>


<BookOpen

className="
mx-auto
text-cyan-400
"

size={36}

/>



<h2

className="
mt-6
text-4xl
font-bold
text-white
md:text-5xl
"

>

Ready to build faster?

</h2>



<p

className="
mx-auto
mt-5
max-w-xl
text-zinc-400
"

>

Explore DevKit commands,
improve your workflow and
ship projects faster.

</p>





<div

className="
mt-10
flex
justify-center
gap-4
"

>


<a

href="/"

className="
rounded-xl
bg-white
px-6
py-3
font-medium
text-black
transition
hover:bg-zinc-200
"

>

Get Started

</a>




<a

href="https://github.com"

className="
flex
items-center
gap-2
rounded-xl
border
border-zinc-800
px-6
py-3
text-white
transition
hover:bg-zinc-900
"

>


<FaGithub size={18}/>

GitHub


</a>


</div>



</motion.div>



</div>



</footer>

);

}