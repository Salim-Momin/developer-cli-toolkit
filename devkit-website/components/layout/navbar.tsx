"use client";

import { motion } from "framer-motion";
import { Menu, X, Download } from "lucide-react";
import { useState, useEffect } from "react";
import { FaGithub } from "react-icons/fa";

const navLinks = [
  {
    name: "Features",
    href: "#features",
  },
  {
    name: "Terminal",
    href: "#terminal",
  },
  {
    name: "Docs",
    href: "#docs",
  },
  {
    name: "Download",
    href: "#download",
  },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };

    window.addEventListener(
      "scroll",
      handleScroll
    );

    return () =>
      window.removeEventListener(
        "scroll",
        handleScroll
      );
  }, []);


  return (
    <>
      <motion.nav
        initial={{
          y: -100,
          opacity: 0,
        }}
        animate={{
          y: 0,
          opacity: 1,
        }}
        transition={{
          duration: 0.6,
        }}
        className={`
          fixed
          top-6
          left-1/2
          -translate-x-1/2
          z-50
          w-[90%]
          max-w-6xl
          rounded-full
          border
          px-6
          py-3
          transition-all
          ${
            scrolled
              ? "bg-black/70 backdrop-blur-xl shadow-xl border-white/10"
              : "bg-white/5 backdrop-blur-md border-white/10"
          }
        `}
      >

        <div className="
          flex
          items-center
          justify-between
        ">

          {/* Logo */}

          <a
            href="#"
            className="
              text-xl
              font-bold
              tracking-tight
              text-white
              hover:text-cyan-400
              transition
            "
          >
            ◉ DevKit
          </a>


          {/* Desktop Menu */}

          <div
            className="
              hidden
              md:flex
              items-center
              gap-8
            "
          >

            {
              navLinks.map((link)=>(
                <a
                  key={link.name}
                  href={link.href}
                  className="
                    text-sm
                    text-zinc-400
                    hover:text-white
                    transition
                    relative
                    group
                  "
                >

                  {link.name}

                  <span
                    className="
                    absolute
                    left-0
                    -bottom-1
                    h-[2px]
                    w-0
                    bg-cyan-400
                    transition-all
                    group-hover:w-full
                    "
                  />

                </a>
              ))
            }

          </div>



          {/* Right Buttons */}

          <div
            className="
            hidden
            md:flex
            items-center
            gap-3
            "
          >

            <a
              href="https://github.com"
              target="_blank"
              className="
              p-2
              rounded-full
              hover:bg-white/10
              transition
              "
            >
              <FaGithub size={20}/>
            </a>


            <a
              href="#download"
              className="
              flex
              items-center
              gap-2
              rounded-full
              bg-white
              text-black
              px-5
              py-2
              text-sm
              font-medium
              hover:scale-105
              transition
              "
            >

              <Download size={16}/>

              Install

            </a>

          </div>



          {/* Mobile Button */}

          <button
            className="
            md:hidden
            text-white
            "
            onClick={() =>
              setOpen(!open)
            }
          >

            {
              open
              ?
              <X/>
              :
              <Menu/>
            }

          </button>


        </div>


      </motion.nav>



      {/* Mobile Menu */}


      {
        open && (

          <motion.div

            initial={{
              opacity:0,
              x:100,
            }}

            animate={{
              opacity:1,
              x:0,
            }}

            className="
            fixed
            right-0
            top-0
            z-40
            h-screen
            w-[80%]
            bg-black
            border-l
            border-white/10
            p-10
            pt-28
            md:hidden
            "

          >

            <div
            className="
            flex
            flex-col
            gap-8
            "
            >

            {
              navLinks.map((link)=>(
                <a
                key={link.name}
                href={link.href}
                onClick={()=>setOpen(false)}
                className="
                text-xl
                text-zinc-300
                hover:text-cyan-400
                "
                >
                  {link.name}
                </a>
              ))
            }


            <a
            href="#download"
            className="
            rounded-full
            bg-white
            text-black
            px-5
            py-3
            text-center
            font-medium
            "
            >
              Install DevKit
            </a>


            </div>


          </motion.div>

        )
      }

    </>
  );
}