"use client";


import {motion} from "framer-motion";


export default function FeatureIndicator({

active

}:{

active:number

}){


const items=[
"PROJECT",
"GIT",
"SEARCH",
"API"
];


return(

<div

className="
fixed
right-8
top-1/2
hidden
-translate-y-1/2
space-y-4
lg:flex
flex-col
"

>


{
items.map((item,index)=>(


<motion.div

key={item}

animate={{

scale:
active===index ? 1.3 : 1,

opacity:
active===index ? 1 : .4

}}


className="
h-2
w-2
rounded-full
bg-cyan-400
"


/>


))
}


</div>

)

}