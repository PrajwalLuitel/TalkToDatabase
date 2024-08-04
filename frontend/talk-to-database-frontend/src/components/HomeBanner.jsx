import { Montserrat_Alternates } from "next/font/google";
import Link from "next/link";

const montserrat = Montserrat_Alternates({
  subsets: ["latin"],
  weight: ["700"],
});

const HomeBanner = () => {
  return (
    <div className="w-full bg-main-banner-background bg-cover bg-fixed text-center">
      <div className="w-[60%] min-h-[100vh] max-md:w-[90%] mx-auto py-[16%] max-md:py-10">
        <div className=" backdrop-blur-xl backdrop-brightness-[85%] rounded-2xl py-10">
          <h1
            className={`text-emerald-200 font-bold text-[3rem] heading-font ${montserrat.className}`}
          >
            Talk To Your Database
          </h1>
          <p className="p-10 text-slate-200 text-[1.5rem]">
            An intelligent system powered by sophisticated Artificial
            Intelligence Technology to assist you to verbally communicate with
            your database with zero technical expertise.
          </p>

          <Link
            href="/#formElement"
            className="rounded-xl text-2xl  text-emerald-300"
          >
          ↓
          </Link>
          </div>
      </div>
    </div>
  );
};

export default HomeBanner;
