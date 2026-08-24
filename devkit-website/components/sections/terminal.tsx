"use client";

import { useState } from "react";
import { Terminal } from "lucide-react";


const commands={

"project info":`

Project:
Developer CLI Toolkit

Language:
Python

Files:
124

Health:
98/100

`,

"git health":`

Repository:
developer-cli-toolkit

Branch:
main

Changes:
Clean

Health:
100%

`,

"doctor":`

Environment Check

✓ Python installed
✓ Git installed
✓ Node installed

System:
Healthy

`,

"api get":`

GET Request

Status:
200 OK

Response:
Success

`

};



export default function TerminalPlayground(){


const [output,setOutput]=useState(
"Ready for command..."
);


return(

<section

id="terminal"

className="
py-32
max-w-5xl
mx-auto
px-6
"

>


<div
className="
mb-12
"
>

<p
className="
font-mono
text-sm
text-zinc-500
"
>
02 / TERMINAL
</p>


<h2
className="
text-4xl
font-semibold
text-white
mt-4
"
>

Try DevKit

inside your browser.

</h2>

</div>




<div
className="
border
border-zinc-800
rounded-xl
overflow-hidden
bg-[#0D0D0D]
"
>


{/* Header */}

<div
className="
flex
items-center
gap-3
px-5
py-3
border-b
border-zinc-800
"
>

<Terminal size={16}/>

<span
className="
font-mono
text-sm
text-zinc-400
"
>
devkit-terminal
</span>


</div>




<div
className="
p-6
font-mono
text-sm
"
>


<div
className="
flex
flex-wrap
gap-3
mb-8
"
>


{

Object.keys(commands).map((cmd)=>(


<button

key={cmd}

onClick={()=>setOutput(commands[cmd as keyof typeof commands])}

className="
border
border-zinc-800
px-4
py-2
rounded-md
text-zinc-400
hover:text-white
hover:border-zinc-500
transition
"

>

$ devkit {cmd}

</button>


))

}


</div>



<pre
className="
text-green-400
whitespace-pre-wrap
"
>

{output}

</pre>



</div>


</div>


</section>

)

}