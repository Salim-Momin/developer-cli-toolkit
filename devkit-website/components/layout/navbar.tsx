"use client";

import { FaGithub } from "react-icons/fa";
import { motion } from "framer-motion";


const links = [
  {
    name:"Features",
    href:"#features"
  },
  {
    name:"Docs",
    href:"#docs"
  },
  {
    name:"Install",
    href:"#install"
  }
];


export default function Navbar(){

return(

<motion.header

initial={{
y:-20,
opacity:0
}}

animate={{
y:0,
opacity:1
}}

transition={{
duration:0.5
}}

className="
fixed
top-0
left-0
right-0
z-50
border-b
border-zinc-800
bg-[#09090B]/80
backdrop-blur-xl
"

>


<div
className="
max-w-6xl
mx-auto
px-6
h-16
flex
items-center
justify-between
"
>


{/* Logo */}

<a
href="/"
className="
font-mono
text-white
font-semibold
tracking-tight
"
>

<span className="text-green-400">
$
</span>

&nbsp;devkit

</a>




{/* Navigation */}

<nav
className="
hidden
md:flex
items-center
gap-8
font-mono
text-sm
"
>

{
links.map((link)=>(

<a

key={link.name}

href={link.href}

className="
text-zinc-400
hover:text-white
transition
"

>

{link.name}

</a>

))

}

</nav>




{/* Github */}

<a

href="https://github.com"

target="_blank"

className="
flex
items-center
gap-2
font-mono
text-sm
text-zinc-400
hover:text-white
transition
"

>

<FaGithub size={16}/>

GitHub

</a>



</div>


</motion.header>


)

}