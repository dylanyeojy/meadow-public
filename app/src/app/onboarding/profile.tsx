import {
    View,
    StyleSheet,
    Text,
    ScrollView,
    KeyboardAvoidingView,
} from "react-native";
import { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { type, colors } from "@/theme";
import { router } from "expo-router";
import { PrimaryButton } from "@/components/primary-button";
import { ProgressBar } from "@/components/progress-bar";
import { PressableScale } from "@/components/pressable-scale";
import { InputField } from "@/components/input-field";

const years = ["1", "2", "3", "4+"];

export default function OnboardingProfileScreen() {
    const [name, setName] = useState("");
    const [university, setUniversity] = useState("");
    const [course, setCourse] = useState("");
    const [year, setYear] = useState<string | null>(null);

    const canContinue =
        name.trim() !== "" &&
        university.trim() !== "" &&
        course.trim() !== "" &&
        year !== null;

    return (
        <SafeAreaView style={styles.screen}>
            <ProgressBar step={2} style={{ marginBottom: 26 }} />
            <KeyboardAvoidingView style={styles.keyboard} behavior="padding">
                <ScrollView
                    contentContainerStyle={styles.middle}
                    keyboardShouldPersistTaps="handled"
                    showsVerticalScrollIndicator={false}
                >
                    <View style={styles.header}>
                        <Text style={styles.title}>A little about you</Text>
                        <Text style={styles.subtitle}>
                            This helps us keep things relevant. You can change
                            it anytime.
                        </Text>
                    </View>
                    <View style={styles.form}>
                        <InputField
                            label="Full name"
                            autoCapitalize="words"
                            autoComplete="name"
                            value={name}
                            onChangeText={setName}
                        />
                        <InputField
                            label="University"
                            autoCapitalize="words"
                            value={university}
                            onChangeText={setUniversity}
                        />
                        <InputField
                            label="Course"
                            autoCapitalize="words"
                            value={course}
                            onChangeText={setCourse}
                        />
                    </View>
                    <View>
                        <Text style={styles.label}>Year of study</Text>
                        <View style={styles.row}>
                            {years.map((y) => (
                                <PressableScale
                                    key={y}
                                    style={[
                                        styles.option,
                                        year === y && styles.optionSelected,
                                    ]}
                                    onPress={() => setYear(y)}
                                >
                                    <Text
                                        style={[
                                            styles.optionText,
                                            year === y &&
                                                styles.optionTextSelected,
                                        ]}
                                    >
                                        {y}
                                    </Text>
                                </PressableScale>
                            ))}
                        </View>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
            <PrimaryButton
                label="Continue"
                onPress={() => router.push("/onboarding/reminders")}
                style={{ marginTop: 20 }}
                disabled={!canContinue}
            />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: colors.sand,
        paddingHorizontal: 24,
        paddingTop: 8,
        paddingBottom: 45, // judge by eye.
    },
    middle: {
        flexGrow: 1,
    },
    header: {
        marginBottom: 28,
    },
    title: {
        ...type.title1,
        color: colors.ink,
        lineHeight: 34,
    },
    subtitle: {
        ...type.body,
        marginTop: 10,
        color: colors.muted,
    },
    keyboard: {
        flex: 1,
    },
    form: {
        gap: 16,
    },
    label: {
        ...type.subhead,
        fontWeight: "500",
        color: colors.muted,
        marginBottom: 7,
        marginTop: 15,
    },
    row: {
        flexDirection: "row",
        gap: 10,
    },
    option: {
        flex: 1,
        alignItems: "center",
        borderRadius: 16,
        paddingVertical: 13,
        backgroundColor: colors.surface,
        borderWidth: 1,
        borderColor: colors.border,
    },
    optionText: {
        ...type.callout,
        fontSize: 16,
        fontWeight: "600",
        color: colors.muted,
    },
    optionSelected: {
        backgroundColor: colors.sageFill,
        borderWidth: 1.5,
        borderColor: colors.sage,
    },
    optionTextSelected: {
        fontWeight: "700",
        color: colors.forest,
    },
});
