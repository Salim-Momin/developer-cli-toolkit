import Hero from "@/components/sections/hero";
import TerminalPlayground from "@/components/sections/terminal";
import InstallSection from "@/components/install/InstallSection";
import FeatureSection from "@/components/features/FeatureSection";
import Footer from "@/components/sections/Footer";

export default function Home(){

return(

<main className="relative z-10">

<Hero/>
<TerminalPlayground/>
<InstallSection />
<FeatureSection/>
<Footer />
</main>

)

}