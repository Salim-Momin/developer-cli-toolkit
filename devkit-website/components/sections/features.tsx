import {
 Terminal,
 Search,
 GitBranch,
 Globe,
 ShieldCheck
} from "lucide-react";


const features=[

{
icon:Terminal,
title:"Project Analyzer",
command:"devkit project info",
description:
"Analyze project structure, languages and health."
},

{
icon:Search,
title:"Smart Search",
command:'devkit search "query"',
description:
"Search code instantly with filters."
},

{
icon:GitBranch,
title:"Git Toolkit",
command:"devkit git health",
description:
"Inspect branches, commits and repository status."
},

{
icon:Globe,
title:"API Tester",
command:"devkit api get URL",
description:
"Test APIs directly from your terminal."
},

{
icon:ShieldCheck,
title:"Environment Doctor",
command:"devkit doctor",
description:
"Check your developer environment."
}

];


export default function Features(){


return(

<section
id="features"
className="
py-32
max-w-6xl
mx-auto
px-6
"
>


<div
className="
mb-16
"
>

<p
className="
font-mono
text-sm
text-zinc-500
"
>
01 / FEATURES
</p>


<h2
className="
mt-4
text-4xl
font-semibold
text-white
"
>

Everything you need

inside terminal.

</h2>


</div>




<div
className="
space-y-6
"
>


{
features.map((item,index)=>{


const Icon=item.icon;


return(

<div

key={item.title}

className="
group
border
border-zinc-800
rounded-xl
p-6
bg-[#0D0D0D]
hover:border-zinc-600
transition
"


>


<div
className="
flex
items-start
gap-5
"
>


<div
className="
p-3
rounded-lg
bg-zinc-900
"
>

<Icon
size={20}
className="text-zinc-300"
/>

</div>



<div>

<h3
className="
text-xl
text-white
font-medium
"
>

{item.title}

</h3>


<p
className="
mt-2
text-zinc-400
"
>

{item.description}

</p>



<div
className="
mt-4
font-mono
text-sm
text-green-400
"
>

$ {item.command}

</div>


</div>


</div>


</div>


)

})
}


</div>


</section>

)

}