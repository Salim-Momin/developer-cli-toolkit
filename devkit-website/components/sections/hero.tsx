"use client";

import { TypeAnimation } from "react-type-animation";
import { motion } from "framer-motion";
import { Terminal} from "lucide-react";
import { FaGithub } from "react-icons/fa";


export default function Hero() {

return (

<section
className="
min-h-screen
flex
items-center
justify-center
bg-[#09090B]
px-6
pt-24
"
>


<div
className="
w-full
max-w-5xl
"
>


{/* Heading */}

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
duration:0.6
}}

className="
text-center
mb-12
"

>


<div
className="
inline-flex
items-center
gap-2
border
border-zinc-800
rounded-full
px-4
py-2
text-sm
text-zinc-400
mb-6
"
>

<Terminal size={15}/>

Developer CLI Toolkit

</div>



<h1
className="
text-5xl
md:text-7xl
font-semibold
tracking-tight
text-white
"
>

Powerful tools.

<br/>

Inside your

<span className="
text-zinc-500
">
terminal.
</span>

</h1>



<p
className="
mt-6
text-zinc-400
max-w-xl
mx-auto
text-lg
"
>

Analyze projects, manage Git,
test APIs and automate developer workflows
without leaving your command line.

</p>


<div
className="
mt-8
flex
justify-center
gap-4
"
>


<button
className="
px-5
py-2.5
rounded-lg
bg-white
text-black
text-sm
font-medium
hover:bg-zinc-200
transition
"
>

Install DevKit

</button>


<button
className="
flex
items-center
gap-2
px-5
py-2.5
rounded-lg
border
border-zinc-800
text-white
hover:bg-zinc-900
transition
"
>

<FaGithub size={16}/>

GitHub

</button>


</div>


</motion.div>





{/* Terminal Window */}


<motion.div

initial={{
opacity:0,
scale:0.95
}}

animate={{
opacity:1,
scale:1
}}

transition={{
duration:0.8
}}

className="
rounded-xl
border
border-zinc-800
bg-[#0D0D0D]
overflow-hidden
shadow-2xl
"

>


{/* Terminal Header */}

<div
className="
flex
items-center
gap-2
px-5
py-3
border-b
border-zinc-800
"
>

<span
className="
w-3
h-3
rounded-full
bg-red-500
"
/>

<span
className="
w-3
h-3
rounded-full
bg-yellow-500
"
/>


<span
className="
w-3
h-3
rounded-full
bg-green-500
"/>


<p
className="
ml-4
text-xs
text-zinc-500
font-mono
"
>
devkit-terminal
</p>


</div>




{/* Terminal Body */}


<div
className="
p-6
font-mono
text-sm
leading-8
text-zinc-300
min-h-[300px]
"
>


<p>
<span className="text-green-400">
$
</span>
&nbsp; devkit
</p>


<div
className="
mt-4
text-white
"
>

<TypeAnimation

sequence={[

"Initializing DevKit...",
1000,

"Loading developer tools...",
1000,

"✓ Project Analyzer ready",
800,

"✓ Git Toolkit ready",
800,

"✓ API Tester ready",
800,

"✓ Environment Doctor ready",
800,

"DevKit is ready 🚀"

]}

speed={50}

/>

</div>


<br/>


<p>
<span className="text-green-400">
$
</span>
&nbsp;
<span className="text-blue-400">
devkit project health
</span>
</p>


<p className="text-green-400">
Health Score: 100/100
</p>


</div>



</motion.div>



</div>


</section>

)

}