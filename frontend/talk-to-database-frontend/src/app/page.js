import HomeBanner from "@/components/HomeBanner";
import DatabaseForm from "@/components/DatabaseForm";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <div>
      <HomeBanner />
        <DatabaseForm id="formElement" />
      <Footer />
    </div>
  );
}
