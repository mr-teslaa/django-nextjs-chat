import { Box, CssBaseline } from "@mui/material";
import { PrimaryAppBar } from "./templates/PrimaryAppBar";
import { PrimaryDraw } from "./templates/PrimaryDraw";

export const Home = () => {
	return (
		<Box sx={{ display: "flex" }}>
			<CssBaseline />
			<PrimaryAppBar />
			<PrimaryDraw></PrimaryDraw>
			Home
		</Box>
	);
};
