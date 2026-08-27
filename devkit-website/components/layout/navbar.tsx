"use client";

import { FaGithub } from "react-icons/fa";
import { motion } from "framer-motion";
import Link from "next/link";


const navLinks = [
{
name:"Home",
href:"#home"
},
{
name:"Terminal",
href:"#terminal"
},
{
name:"Features",
href:"#features"
},
{
name:"Install",
href:"#installation"
},
{
name:"Docs",
href:"/docs"
}
];


const DEVKIT_LOGO = `
██████╗ ███████╗██╗   ██╗██╗  ██╗██╗████████╗
██╔══██╗██╔════╝██║   ██║██║ ██╔╝██║╚══██╔══╝
██║  ██║█████╗  ██║   ██║█████╔╝ ██║   ██║
██║  ██║██╔══╝  ╚██╗ ██╔╝██╔═██╗ ██║   ██║
██████╔╝███████╗ ╚████╔╝ ██║  ██╗██║   ██║
╚═════╝ ╚══════╝  ╚═══╝  ╚═╝  ╚═╝╚═╝   ╚═╝
`;


export default function Navbar() {


return (

<motion.header

initial={{
opacity:0,
y:-20,
}}

animate={{
opacity:1,
y:0,
}}

transition={{
duration:0.5,
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
max-w-7xl
mx-auto
px-6
h-20
flex
items-center
justify-between
"

>


{/* LOGO */}

<Link href="/">

<motion.div

whileHover={{
scale:1.05,
}}

transition={{
duration:0.2,
}}

className="
hidden
md:block
font-mono
text-[7px]
leading-[7px]
text-cyan-400
drop-shadow-[0_0_15px_rgba(34,211,238,0.7)]
hover:text-white
transition
duration-300
cursor-pointer
"

>

<pre>

{DEVKIT_LOGO}

</pre>


</motion.div>



{/* Mobile Logo */}

<div

className="
md:hidden
font-mono
text-green-400
text-sm
"

>

devkit_

</div>


</Link>





{/* NAV LINKS */}

<nav

className="
hidden
lg:flex
items-center
gap-8
font-mono
text-sm
"

>


{

navLinks.map((link)=>(


<motion.div

key={link.name}

whileHover={{
y:-2,
}}

transition={{
duration:0.2,
}}

>

<Link

href={link.href}

className="
text-zinc-400
hover:text-white
transition
"

>

{link.name}

</Link>


</motion.div>


))

}


</nav>





{/* RIGHT SIDE */}

<motion.a

href="https://github/Salim-Momin.com"

target="_blank"

whileHover={{
scale:1.08,
}}

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


<span className="
hidden
sm:block
">

GitHub

</span>


</motion.a>



</div>


</motion.header>


);

}