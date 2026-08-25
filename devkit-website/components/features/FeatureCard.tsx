"use client";

import { motion, useScroll, useTransform, useSpring } from "framer-motion";
import { useRef } from "react";

import FeatureTerminal from "./FeatureTerminal";


type Props = {
  title: string;
  description: string;
  icon: string;
  points: string[];
  type: string;
  reverse: boolean;
};



export default function FeatureCard({
  title,
  description,
  icon,
  points,
  type,
  reverse,
}: Props) {


  const cardRef = useRef<HTMLDivElement>(null);


  // Scroll Camera Animation

  const { scrollYProgress } = useScroll({

    target: cardRef,

    offset: [
      "start end",
      "center center"
    ],

  });



  const progress = useSpring(
    scrollYProgress,
    {
      stiffness: 80,
      damping: 25,
      mass: 0.5,
    }
  );



  const scale = useTransform(
    progress,
    [0, 1],
    [0.82, 1]
  );


  const rotateX = useTransform(
    progress,
    [0, 1],
    [18, 0]
  );


  const translateY = useTransform(
    progress,
    [0, 1],
    [120, 0]
  );


  const opacity = useTransform(
    progress,
    [0, 1],
    [0, 1]
  );





  return (


    <motion.div

      ref={cardRef}


      style={{

        scale,

        rotateX,

        y: translateY,

        opacity,

        transformPerspective: 1400,

      }}



      className={`
        grid
        items-center
        gap-14
        md:grid-cols-2
        lg:gap-20

        transition={{
duration:0.8,
ease:"easeOut"
}}

        ${
          reverse
          ? "md:[&>*:first-child]:order-2"
          : ""
        }

      `}


    >



      {/* TEXT SECTION */}


      <motion.div


        initial={{

          opacity:0,

          x: reverse ? 80 : -80,

        }}


        whileInView={{

          opacity:1,

          x:0,

        }}


        viewport={{

          once:true,

          amount:.3,

        }}


        transition={{

          duration:.8,

          ease:"easeOut",

        }}



      >



        <div className="mb-6 flex items-center gap-4">


          <div

            className="
            flex
            h-14
            w-14
            items-center
            justify-center
            rounded-2xl
            border
            border-cyan-500/20
            bg-cyan-500/10
            text-2xl
            shadow-lg
            shadow-cyan-500/10
            "

          >

            {icon}


          </div>



          <h3

            className="
            text-3xl
            font-bold
            text-white
            md:text-4xl
            "

          >

            {title}


          </h3>



        </div>





        <p

          className="
          max-w-xl
          text-lg
          leading-relaxed
          text-zinc-400
          "

        >

          {description}


        </p>





        <div

          className="
          mt-8
          space-y-4
          "

        >


          {
            points.map((point,index)=>(


              <motion.div


                key={point}


                initial={{

                  opacity:0,

                  x:-20,

                }}


                whileInView={{

                  opacity:1,

                  x:0,

                }}


                viewport={{

                  once:true,

                }}


                transition={{

                  delay:index * .1,

                }}



                className="
                flex
                items-center
                gap-3
                text-zinc-300
                "

              >


                <span

                  className="
                  h-2
                  w-2
                  rounded-full
                  bg-cyan-400
                  shadow-[0_0_12px_#22d3ee]
                  "

                />


                {point}


              </motion.div>


            ))
          }



        </div>



      </motion.div>







      {/* TERMINAL SECTION */}



      <motion.div


        initial={{

          opacity:0,

          scale:.7,

          rotateY:20,

        }}



        whileInView={{

          opacity:1,

          scale:1,

          rotateY:0,

        }}



        viewport={{

          once:true,

          amount:.3,

        }}



        transition={{

          duration:1,

          ease:"easeOut",

        }}



        whileHover={{

          y:-10,

        }}



        className="
        relative
        "

      >


        <FeatureTerminal

          type={type}

        />


      </motion.div>




    </motion.div>


  );

}