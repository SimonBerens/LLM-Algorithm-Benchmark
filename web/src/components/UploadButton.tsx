import {FileUploader} from "react-drag-drop-files";
import {ResultsFile, resultsFileSchema} from "@/schema";

interface UploadButtonProps {
    setFileJson: (newJsonString: ResultsFile) => void
}

export function UploadButton({setFileJson}: UploadButtonProps) {

    return (
        <FileUploader types={["JSON"]} handleChange={async (file: File) => {
            const fileString = await file.text()
            setFileJson(resultsFileSchema.parse(JSON.parse(fileString)))
            console.log("success!")
        }
        }/>
    )
}