import {type NextPage} from "next";
import {CollapsibleTable} from "@/components/CollapsibleTable";
import {UploadButton} from "@/components/UploadButton";
import {useState} from "react";
import {ResultsFile} from "@/schema";

const Home: NextPage = () => {
    const [fileJson, setFileJson] = useState<ResultsFile | null>(null)
    return (
        <>
            <UploadButton setFileJson={setFileJson}/>
            {fileJson !== null && <CollapsibleTable fileJson={fileJson}/>}
        </>
    );
};

export default Home;
