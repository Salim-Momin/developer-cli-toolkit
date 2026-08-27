"use client";

import { motion } from "framer-motion";
import { FaGithub } from "react-icons/fa";
import { Terminal } from "lucide-react";


export default function Footer(){

return (

<footer

className="
relative
overflow-hidden
border-t
border-zinc-800
py-16
"

>


{/* Background */}

<div className="absolute inset-0">
  
<div
className="
absolute
top-0
left-1/2
h-px
w-[70%]
-translate-x-1/2
bg-gradient-to-r
from-transparent
via-cyan-400/70
to-transparent
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

opacity:[
0.3,
0.7,
0.3
],

scale:[
0.9,
1.1,
0.9
]

}}

transition={{

duration:6,
repeat:Infinity,
ease:"easeInOut"

}}

className="
absolute
bottom-0
left-1/2
-translate-x-1/2
h-40
w-[70%]
rounded-full
bg-cyan-500/20
blur-[120px]
"

/>


</div>




<div

className="
relative
z-10
mx-auto
max-w-7xl
px-6
"

>


<div

className="
grid
gap-10
md:grid-cols-3
"

>


{/* Brand */}

<div>


<div

className="
flex
items-center
gap-2
text-white
font-semibold
"

>

<Terminal size={18}/>

DevKit

</div>



<p

className="
mt-4
max-w-sm
text-sm
leading-relaxed
text-zinc-500
"

>

Developer CLI Toolkit for analyzing,
debugging and automating developer
workflows directly from your terminal.

</p>


</div>






{/* Links */}

<div>

<h3

className="
text-sm
font-medium
text-white
"

>

Explore

</h3>


<div

className="
mt-4
space-y-3
text-sm
text-zinc-500
"

>


<a
href="#home"
className="block hover:text-cyan-400 transition"
>
Home
</a>


<a
href="#features"
className="block hover:text-cyan-400 transition"
>
Features
</a>


<a
href="#terminal"
className="block hover:text-cyan-400 transition"
>
Terminal
</a>


<a
href="#installation"
className="block hover:text-cyan-400 transition"
>
Installation
</a>


</div>

</div>







{/* Community */}

<div>


<h3

className="
text-sm
font-medium
text-white
"

>

Community

</h3>



<a

href="#"

className="
mt-4
flex
items-center
gap-2
text-sm
text-zinc-500
hover:text-cyan-400
transition
"

>

<FaGithub/>

GitHub

</a>



<p

className="
mt-6
font-mono
text-xs
text-zinc-600
"

>

DevKit v0.1.5

</p>
<br></br>
<p className="font-mono text-xs text-zinc-500">
    Crafted by <span className="text-cyan-400 font-medium">Salim Momin</span>
</p>

</div>



</div>





{/* Bottom */}

<div

className="
mt-12
border-t
border-zinc-800
pt-6
text-center
text-xs
text-zinc-600
"

>

© 2026 DevKit.
Build • Debug • Analyze • Automate

</div>



</div>

<motion.div

animate={{

scale:[1,1.15,1],

opacity:[.3,.6,.3]

}}

transition={

{

duration:8,

repeat:Infinity

}

}

className="
absolute
bottom-0
left-1/2
h-56
w-[700px]
-translate-x-1/2
rounded-full
bg-cyan-500/10
blur-[140px]
"
/>


</footer>

);

} 