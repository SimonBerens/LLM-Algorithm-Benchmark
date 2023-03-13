import * as React from 'react';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import {ResultsFile} from "@/schema";
import {BasicModal} from "@/components/BasicModal";
import {useState} from "react";

type RawResults = ResultsFile["results"]

interface TaskPrediction {
    correct: number
    total: number
}

interface RowProps {
    llmName: string,
    predictions: TaskPrediction[]
    rawResults: RawResults
    inputTexts: ResultsFile["input_texts"]
}

function Row({llmName, predictions, rawResults, inputTexts}: RowProps) {
    const [collapsed, setCollapsed] = useState(true)
    const [modalOpen, setModalOpen] = useState(false)
    const [modalTitle, setModalTitle] = useState("")
    const [modalBody, setModalBody] = useState("")

    return (
        <React.Fragment>
            <TableRow sx={{'& > *': {borderBottom: 'unset'}}}>
                <TableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        onClick={() => setCollapsed(!collapsed)}
                    >
                        {!collapsed ? <KeyboardArrowUpIcon/> : <KeyboardArrowDownIcon/>}
                    </IconButton>
                </TableCell>
                <TableCell component="th" scope="row">
                    {llmName}
                </TableCell>
                {predictions.map(({correct, total}) => <TableCell align="right">{correct} / {total}</TableCell>)}
            </TableRow>
            <TableRow>
                <TableCell style={{paddingBottom: 0, paddingTop: 0}} colSpan={6}>
                    <Collapse in={!collapsed} timeout="auto" unmountOnExit>
                        <Box sx={{margin: 1}}>
                            <Typography variant="h6" gutterBottom component="div">
                                All results for {llmName}
                            </Typography>
                            <Table size="small" aria-label={`All results for ${llmName}`}>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Task</TableCell>
                                        <TableCell>Input</TableCell>
                                        <TableCell align="right">Predicted Output</TableCell>
                                        <TableCell align="right">True Output</TableCell>
                                        <TableCell align="right">Correct</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {rawResults.map((result) => {
                                        return (
                                            <TableRow key={result.task_info_key}>
                                                <TableCell component="th" scope="row">
                                                    {result.task_info_key}
                                                </TableCell>
                                                <button onClick={() => {
                                                    setModalOpen(true)
                                                    setModalTitle(result.input_text_key)
                                                    setModalBody(inputTexts[result.input_text_key]!)
                                                }}>
                                                    <TableCell>{result.input_text_key}</TableCell>
                                                </button>
                                                <TableCell align="right">{result.predicted_output}</TableCell>
                                                <TableCell align="right">{result.code_output}</TableCell>
                                                <TableCell
                                                    align="right">{result.correctly_predicted ? "Yes" : "No"}</TableCell>
                                            </TableRow>
                                        );
                                    })}
                                </TableBody>
                            </Table>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
            <BasicModal open={modalOpen} setOpen={setModalOpen} title={modalTitle} body={modalBody}/>
        </React.Fragment>
    );
}

interface CollapsibleTableProps {
    fileJson: ResultsFile
}

function getTotalStats(predictions: TaskPrediction[]): TaskPrediction {
    return predictions.reduce(({correct, total}, acc) => ({correct: acc.correct + correct, total: acc.total + total}))
}

export function CollapsibleTable({fileJson}: CollapsibleTableProps) {
    const llmNames = [...new Set(fileJson.results.map(result => result.llm_executor_name))]
    const perLlmStats: Record<string, { taskSummaries: Record<string, TaskPrediction>, rawResults: RawResults }> = {}
    for (const result of fileJson.results) {
        if (perLlmStats[result.llm_executor_name] === undefined) {
            perLlmStats[result.llm_executor_name] = {taskSummaries: {}, rawResults: []}
        }
        if (perLlmStats[result.llm_executor_name]!.taskSummaries[result.task_info_key] === undefined) {
            perLlmStats[result.llm_executor_name]!.taskSummaries[result.task_info_key] = {correct: 0, total: 0}
        }
        perLlmStats[result.llm_executor_name]!.taskSummaries[result.task_info_key]!.correct += result.correctly_predicted ? 1 : 0
        perLlmStats[result.llm_executor_name]!.taskSummaries[result.task_info_key]!.total++
        perLlmStats[result.llm_executor_name]!.rawResults.push(result)
    }
    return (
        <TableContainer component={Paper}>
            <Table aria-label="collapsible table">
                <TableHead>
                    <TableRow>
                        <TableCell/>
                        <TableCell>LLM</TableCell>
                        <TableCell align="right">Total</TableCell>
                        {Object.keys(fileJson.task_infos).map(key => (
                            <TableCell align="right">{key}</TableCell>
                        ))}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {llmNames.map(llmName => {
                        const llmPredictions = Object.values(perLlmStats[llmName]!.taskSummaries);
                        const totalStats = getTotalStats(llmPredictions)
                        const rawResults = perLlmStats[llmName]!.rawResults
                        return (
                            <Row llmName={llmName} predictions={[totalStats, ...llmPredictions]}
                                 rawResults={rawResults} inputTexts={fileJson.input_texts}/>
                        )
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    );
}