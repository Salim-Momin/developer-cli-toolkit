"use client";

import { motion } from "framer-motion";

import InstallCard from "./InstallCard";
import QuickCommand from "./QuickCommand";

export default function InstallSection() {
  return (
    <section id="installation" className="relative overflow-hidden py-32">
      {/* Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,#06b6d420,transparent_60%)]" />

        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.02)_1px,transparent_1px)] bg-[size:64px_64px]" />

        <div className="absolute left-20 top-10 h-96 w-96 rounded-full bg-cyan-500/10 blur-[160px]" />

        <div className="absolute right-0 bottom-0 h-[500px] w-[500px] rounded-full bg-blue-500/10 blur-[180px]" />
      </div>

      <div className="relative mx-auto max-w-7xl px-6">
        {/* Header */}

        <motion.div
          initial={{ opacity: 0, y: 60 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: .8 }}
          className="text-center"
        >
          <p className="mb-4 uppercase tracking-[0.4em] text-cyan-400">
            Getting Started
          </p>

          <h2 className="text-5xl font-bold text-white md:text-6xl">
            Install DevKit
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-lg text-zinc-400">
            Install DevKit in seconds and start analyzing projects,
            inspecting Git repositories, testing APIs and searching
            code directly from your terminal.
          </p>
        </motion.div>

        {/* Install Cards */}

        <motion.div
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
        variants={{
            hidden: {},
            show: {
            transition: {
                staggerChildren: 0.15,
            },
            },
        }}
        className="mt-20 grid gap-8 lg:grid-cols-2"
        >
        <motion.div
            variants={{
            hidden: {
                opacity: 0,
                y: 40,
            },
            show: {
                opacity: 1,
                y: 0,
            },
            }}
        >
            <InstallCard
            title="PIP"
            command="pip install developer-cli-toolkit"
            />
        </motion.div>

        <motion.div
            variants={{
            hidden: {
                opacity: 0,
                y: 40,
            },
            show: {
                opacity: 1,
                y: 0,
            },
            }}
        >
            <InstallCard
            title="GitHub"
            command="git clone https://github.com/Salim-Momin/developer-cli-toolkit"
            />
        </motion.div>
        </motion.div>

        {/* Quick Commands */}

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ delay: .2 }}
          viewport={{ once: true }}
          className="mt-24"
        >
          <h3 className="mb-10 text-center text-3xl font-semibold text-white">
            Quick Commands
          </h3>

          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            <QuickCommand
              title="Environment"
              command="devkit doctor"
            />

            <QuickCommand
              title="Project"
              command="devkit project info"
            />

            <QuickCommand
              title="Search"
              command='devkit search "TODO"'
            />

            <QuickCommand
              title="Git"
              command="devkit git status"
            />
          </div>
        </motion.div>
      </div>
      {/* Section Bottom Merge Glow */}

<div

className="
pointer-events-none
absolute
bottom-0
left-1/2
-translate-x-1/2
h-32
w-[80%]
rounded-full
bg-cyan-500/10
blur-[100px]
"

/>
    </section>
  );
}