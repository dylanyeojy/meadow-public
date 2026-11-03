import * as SplashScreen from "expo-splash-screen";
import { useFonts } from "expo-font";
import { useEffect } from "react";
import { Stack } from "expo-router";

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
    const [loaded, error] = useFonts([
        {
            fontFamily: "PlusJakartaSans",
            fontDefinitions: [
                {
                    path: require("@/assets/fonts/PlusJakartaSans-Regular.ttf"),
                    weight: 400,
                },
                {
                    path: require("@/assets/fonts/PlusJakartaSans-Medium.ttf"),
                    weight: 500,
                },
                {
                    path: require("@/assets/fonts/PlusJakartaSans-SemiBold.ttf"),
                    weight: 600,
                },
                {
                    path: require("@/assets/fonts/PlusJakartaSans-Bold.ttf"),
                    weight: 700,
                },
            ],
        },
        {
            fontFamily: "Lora",
            fontDefinitions: [
                { path: require("@/assets/fonts/Lora.ttf"), weight: 400 },
                {
                    path: require("@/assets/fonts/Lora-Italic.ttf"),
                    weight: 400,
                    style: "italic",
                },
            ],
        },
    ]);

    useEffect(() => {
        if (loaded || error) {
            SplashScreen.hideAsync();
        }
    }, [loaded, error]);

    if (!loaded && !error) {
        return null;
    }

    return <Stack screenOptions={{ headerShown: false }} />;
}
