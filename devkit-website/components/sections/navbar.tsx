"use client";

import { useState } from "react";

import { FaGithub } from "react-icons/fa";
import { motion, AnimatePresence } from "framer-motion";
import { Menu, X } from "lucide-react";
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


const [open,setOpen] = useState(false);



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
bg-black/40
backdrop-blur-2xl
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

className="
hidden
md:block
font-mono
text-[7px]
leading-[7px]
text-cyan-400
drop-shadow-[0_0_15px_rgba(34,211,238,.7)]
"

>


<pre>
{DEVKIT_LOGO}
</pre>


</motion.div>

{/* Mobile Logo */}

<motion.div

whileHover={{
scale:1.05,
}}

className="
md:hidden
w-[140px]
font-mono
text-[3px]
leading-[3px]
text-cyan-400
drop-shadow-[0_0_10px_rgba(34,211,238,.7)]
overflow-hidden
"

>

<pre>
{DEVKIT_LOGO}
</pre>

</motion.div>

</Link>


{/* Desktop Navigation */}


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
y:-2
}}

>

<Link

href={link.href}

className="
text-zinc-400
transition
hover:text-cyan-400
"

>

{link.name}

</Link>


</motion.div>


))

}


</nav>







{/* Right Actions */}


<div

className="
flex
items-center
gap-3
"

>



{/* Github */}


<motion.a

href="https://github.com/Salim-Momin/developer-cli-toolkit"

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
border-cyan-500/20
bg-cyan-500/5
px-4
py-2
text-sm
text-cyan-300
hover:border-cyan-400
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







{/* Mobile Menu Button */}


<button

onClick={()=>setOpen(!open)}

className="
lg:hidden
rounded-xl
border
border-zinc-800
bg-black/40
p-2
text-zinc-300
"

>


{
open ?

<X size={22}/>

:

<Menu size={22}/>

}


</button>



</div>



</div>







{/* Mobile Menu */}


<AnimatePresence>


{

open && (


<motion.div

initial={{
opacity:0,
height:0
}}

animate={{
opacity:1,
height:"auto"
}}

exit={{
opacity:0,
height:0
}}

transition={{
duration:.3
}}

className="
lg:hidden
border-t
border-zinc-800
bg-black/80
backdrop-blur-xl
overflow-hidden
"

>


<div

className="
flex
flex-col
gap-6
px-6
py-8
font-mono
"

>


{

navLinks.map((link)=>(


<Link

key={link.name}

href={link.href}

onClick={()=>setOpen(false)}

className="
text-zinc-400
transition
hover:text-cyan-400
"

>

{link.name}

</Link>


))

}


</div>



</motion.div>


)

}


</AnimatePresence>



</motion.header>

);

}