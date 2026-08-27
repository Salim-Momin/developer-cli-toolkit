"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Copy, Check } from "lucide-react";


const systems = {

Windows: 
`pip install developer-cli-toolkit

devkit --help

devkit doctor
`,

macOS:
`pip install developer-cli-toolkit

devkit --help

devkit doctor
`,

Linux:
`pip install developer-cli-toolkit

devkit --help

devkit doctor
`

};



export default function InstallationGuide(){


const [active,setActive] =
useState("Windows");


const [copied,setCopied] =
useState(false);



function copy(){

navigator.clipboard.writeText(
systems[active as keyof typeof systems]
);


setCopied(true);


setTimeout(()=>{

setCopied(false);

},1500);

}



return (

<section

className="
relative
mx-auto
mt-32
max-w-6xl
px-6
"

>


{/* Heading */}

<motion.div

initial={{
opacity:0,
y:30
}}

whileInView={{
opacity:1,
y:0
}}

viewport={{
once:true
}}

className="
text-center
"

>


<p

className="
font-mono
text-sm
tracking-widest
text-cyan-400
"

>

GETTING STARTED

</p>


<h2

className="
mt-5
text-4xl
font-bold
text-white
md:text-6xl
"

>

Install DevKit

</h2>


<p

className="
mx-auto
mt-5
max-w-xl
text-zinc-400
"

>

Start analyzing projects and automate
your developer workflow in minutes.

</p>


</motion.div>





{/* Tabs */}


<div

className="
mt-12
flex
justify-center
gap-3
"

>


{

Object.keys(systems).map((system)=>(


<button


key={system}


onClick={()=>setActive(system)}


className={`

rounded-full

px-5

py-2

font-mono

text-sm

transition


${

active===system

?

"bg-cyan-500 text-black"

:

"border border-zinc-800 text-zinc-400 hover:text-white"

}

`}


>

{system}

</button>


))


}


</div>






{/* Terminal */}


<motion.div

initial={{

opacity:0,

scale:.95

}}

whileInView={{

opacity:1,

scale:1

}}

viewport={{

once:true

}}

transition={{

duration:.6

}}

className="
mt-10
overflow-hidden
rounded-2xl
border
border-zinc-800
bg-[#050505]
shadow-2xl
"

>


{/* Header */}

<div

className="
flex
items-center
justify-between
border-b
border-zinc-800
px-5
py-4
"

>


<div

className="
flex
gap-2
"

>

<span className="
h-3
w-3
rounded-full
bg-red-500
"/>


<span className="
h-3
w-3
rounded-full
bg-yellow-500
"/>


<span className="
h-3
w-3
rounded-full
bg-green-500
"/>


</div>





<button

onClick={copy}

className="
flex
items-center
gap-2
text-sm
text-zinc-400
hover:text-white
"

>


{

copied

?

<Check size={16}/>

:

<Copy size={16}/>

}


{

copied

?

"Copied"

:

"Copy"

}


</button>



</div>






<pre

className="
p-8
overflow-x-auto
font-mono
text-sm
leading-8
text-cyan-300
"

>

{systems[active as keyof typeof systems]}

</pre>



</motion.div>





</section>

);

}