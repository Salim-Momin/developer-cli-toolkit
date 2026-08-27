"use client";

import { motion } from "framer-motion";


const docs = [

{
title:"Getting Started",
description:
"Install DevKit and learn the basic workflow.",
icon:"🚀",
},

{
title:"Project Commands",
description:
"Analyze projects with information, statistics and tree tools.",
icon:"📦",
},

{
title:"Project Health",
description:
"Check project quality and receive improvement suggestions.",
icon:"❤️",
},

{
title:"Project Tree",
description:
"Explore your complete project structure directly from terminal.",
icon:"🌳",
},

{
title:"Smart Search",
description:
"Search source code with filters and regex support.",
icon:"🔎",
},

{
title:"Environment Doctor",
description:
"Check developer tools, versions and system configuration.",
icon:"🩺",
},

{
title:"Git Toolkit",
description:
"Manage repository status, branches and history.",
icon:"🌿",
},

{
title:"API Tester",
description:
"Test HTTP requests directly from your CLI.",
icon:"🌐",
},

];



export default function DocsCards(){


return (

<section

className="
relative
mx-auto
mt-28
max-w-6xl
px-6
"

>


<div

className="
grid
gap-6
md:grid-cols-2
"

>


{

docs.map((doc,index)=>(


<motion.div


key={doc.title}


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

duration:.6,

delay:index*.08

}}


whileHover={{

y:-8,

scale:1.02

}}



className="
group
relative
overflow-hidden
rounded-2xl
border
border-zinc-800
bg-black/40
p-8
backdrop-blur
transition
"

>


{/* Hover glow */}

<div

className="
absolute
inset-0
bg-gradient-to-br
from-cyan-500/10
to-blue-500/10
opacity-0
transition
duration-500
group-hover:opacity-100
"

/>



<div

className="
relative
"

>


<div

className="
text-3xl
"

>

{doc.icon}

</div>



<h3

className="
mt-5
text-xl
font-semibold
text-white
"

>

{doc.title}

</h3>



<p

className="
mt-3
leading-relaxed
text-zinc-400
"

>

{doc.description}

</p>



<div

className="
mt-6
font-mono
text-sm
text-cyan-400
opacity-0
transition
group-hover:opacity-100
"

>

Read documentation →

</div>



</div>



</motion.div>



))


}



</div>



</section>

);

}