import { View, StyleSheet, Text, ScrollView } from "react-native";
import { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { type, colors } from "@/theme";
import { router } from "expo-router";
import { PrimaryButton } from "@/components/primary-button";
import { ProgressBar } from "@/components/progress-bar";
import { PressableScale } from "@/components/pressable-scale";
import { Toggle } from "@/components/toggle";
import * as icons from "@/components/icons";
import Animated, {
    Easing,
    FadeOut,
    LinearTransition,
    ReduceMotion,
} from "react-native-reanimated";
import { DateTimePickerAndroid } from "@react-native-community/datetimepicker";

// Removing a time: the row fades out and the rows below slide up.
// Under reduced motion the fade stays and the slide is skipped.
const easeOut = Easing.bezier(0.23, 1, 0.32, 1);
const rowExit = FadeOut.duration(200)
    .easing(easeOut)
    .reduceMotion(ReduceMotion.Never);
const rowSlide = LinearTransition.duration(200).easing(easeOut);

const dayLetters = ["S", "M", "T", "W", "T", "F", "S"];
const DAILY = [true, true, true, true, true, true, true];
const WEEKDAYS = [false, true, true, true, true, true, false];
const WEEKENDS = [true, false, false, false, false, false, true];
const NONE = [false, false, false, false, false, false, false];
const presetNames = ["Daily", "Weekdays", "Weekends", "Custom"];

function sameArray(a: boolean[], b: boolean[]) {
    return a.every((value, i) => value === b[i]);
}

function presetOf(picked: boolean[]) {
    if (sameArray(picked, DAILY)) return "Daily";
    if (sameArray(picked, WEEKDAYS)) return "Weekdays";
    if (sameArray(picked, WEEKENDS)) return "Weekends";
    if (!picked.some((p) => p)) return "None";
    return "Custom";
}

function formatTime(time: string) {
    const [hour, minute] = time.split(":");
    const numberedHour = Number(hour);
    const suffix = numberedHour >= 12 && numberedHour <= 23 ? "pm" : "am";
    const displayHour = numberedHour % 12 || 12;

    return `${displayHour}:${minute} ${suffix}`;
}

function toDate(time: string) {
    const [hour, minute] = time.split(":");
    const date = new Date();
    date.setHours(Number(hour), Number(minute), 0, 0);
    return date;
}

function toTimeString(date: Date) {
    const hour = String(date.getHours()).padStart(2, "0");
    const minute = String(date.getMinutes()).padStart(2, "0");

    return `${hour}:${minute}`;
}

export default function OnboardingRemindersScreen() {
    const [remindersOn, setRemindersOn] = useState(false);
    const [days, setDays] = useState(NONE);
    const currentPreset = presetOf(days);
    const [times, setTimes] = useState<string[]>([]);

    const canFinish = remindersOn && times.length > 0;

    // Turning reminders on starts the list at 9:00 am, unless a time is already there.
    function addDefaultTime() {
        if (times.length === 0) setTimes(["09:00"]);
    }

    function handleToggle(next: boolean) {
        setRemindersOn(next);
        setDays(next ? DAILY : NONE);
        if (next) {
            addDefaultTime();
        } else {
            setTimes([]);
        }
    }

    function toggleDay(index: number) {
        const next = [...days]; // copy the days array.
        next[index] = !next[index]; // flip one
        setDays(next); // hand React the new array
        const anyDayOn = next.some((d) => d);
        setRemindersOn(anyDayOn);
        if (anyDayOn) {
            addDefaultTime();
        } else {
            setTimes([]);
        }
    }

    function choosePreset(name: string) {
        if (name === "Daily") setDays(DAILY);
        if (name === "Weekdays") setDays(WEEKDAYS);
        if (name === "Weekends") setDays(WEEKENDS);
        if (name === "Custom") return;
        setRemindersOn(true);
        addDefaultTime();
    }

    function removeTime(time: string) {
        setTimes(times.filter((t) => t !== time));
    }

    function saveTime(picked: string, oldTime?: string) {
        const others = times.filter((t) => t !== oldTime);
        if (others.includes(picked)) return;
        setTimes([...others, picked].sort());

        if (!remindersOn) {
            setRemindersOn(true);
            setDays(DAILY);
        }
    }

    function openPicker(oldTime?: string) {
        DateTimePickerAndroid.open({
            value: oldTime ? toDate(oldTime) : new Date(),
            mode: "time",
            is24Hour: false,
            onChange: (event, picked) => {
                if (event.type !== "set" || !picked) return;
                saveTime(toTimeString(picked), oldTime);
            },
        });
    }

    return (
        <SafeAreaView style={styles.screen}>
            <ProgressBar step={3} style={{ marginBottom: 26 }} />
            <ScrollView
                contentContainerStyle={styles.middle}
                keyboardShouldPersistTaps="handled"
                showsVerticalScrollIndicator={false}
            >
                <View style={styles.header}>
                    <Text style={styles.title}>Gentle reminders</Text>
                    <Text style={styles.subtitle}>
                        A soft nudge to check in. No pressure. You're in
                        control.
                    </Text>
                </View>

                <View style={styles.reminderCard}>
                    <View>
                        <Text style={styles.cardTitle}>Daily reminders</Text>
                        <Text style={styles.cardSubtitle}>
                            {remindersOn ? "On" : "Off"}
                        </Text>
                    </View>
                    <Toggle value={remindersOn} onChange={handleToggle} />
                </View>
                <Text style={styles.sectionLabel}>How often</Text>
                <View style={styles.presetRow}>
                    {presetNames.map((name) => (
                        <PressableScale
                            key={name}
                            onPress={() => choosePreset(name)}
                            style={[
                                styles.pill,
                                currentPreset === name && styles.pillOn,
                            ]}
                        >
                            <Text
                                style={[
                                    styles.pillText,
                                    currentPreset === name && styles.pillTextOn,
                                ]}
                            >
                                {name}
                            </Text>
                        </PressableScale>
                    ))}
                </View>
                <View style={styles.dayRow}>
                    {dayLetters.map((letter, index) => (
                        <PressableScale
                            key={index}
                            style={styles.dayTap}
                            onPress={() => toggleDay(index)}
                        >
                            <View
                                style={[
                                    styles.dayDot,
                                    days[index] && styles.dayDotOn,
                                ]}
                            >
                                <Text
                                    style={[
                                        styles.dayText,
                                        days[index] && styles.dayTextOn,
                                    ]}
                                >
                                    {letter}
                                </Text>
                            </View>
                        </PressableScale>
                    ))}
                </View>
                <Text style={styles.sectionLabel}>Reminder Time</Text>
                <View style={styles.timeList}>
                    {times.map((time) => (
                        <Animated.View
                            style={styles.timeCard}
                            key={time}
                            exiting={rowExit}
                            layout={rowSlide}
                        >
                            <View style={styles.timeLabel}>
                                <icons.ClockIcon
                                    color={colors.sage}
                                    size={18}
                                />
                                <Text style={styles.timeText}>
                                    {formatTime(time)}
                                </Text>
                            </View>
                            <PressableScale
                                style={styles.iconTap}
                                accessibilityLabel={`Change ${formatTime(time)}`}
                                onPress={() => openPicker(time)}
                            >
                                <View
                                    style={[
                                        styles.iconCircle,
                                        styles.editCircle,
                                    ]}
                                >
                                    <icons.PencilIcon
                                        color={colors.sageDeep}
                                        size={16}
                                    />
                                </View>
                            </PressableScale>
                            <PressableScale
                                style={styles.iconTap}
                                onPress={() => removeTime(time)}
                                accessibilityLabel={`Remove ${formatTime(time)}`}
                            >
                                <View
                                    style={[
                                        styles.iconCircle,
                                        styles.deleteCircle,
                                    ]}
                                >
                                    <icons.TrashIcon
                                        color={colors.surface}
                                        size={16}
                                    />
                                </View>
                            </PressableScale>
                        </Animated.View>
                    ))}
                    {times.length < 4 && (
                        <Animated.View layout={rowSlide}>
                            <PressableScale
                                style={styles.addRow}
                                onPress={() => openPicker()}
                            >
                                <icons.PlusIcon
                                    color={colors.muted}
                                    size={16}
                                />
                                <Text style={styles.addRowText}>Add time</Text>
                            </PressableScale>
                        </Animated.View>
                    )}
                </View>
            </ScrollView>
            <PrimaryButton
                label="Finish setup"
                onPress={() => router.replace("/")}
                style={{ marginTop: 20 }}
                disabled={!canFinish}
            />
            <PressableScale
                hitSlop={{
                    top: 14,
                    bottom: 14,
                    left: 8,
                    right: 8,
                }}
                style={styles.skipButton}
                onPress={() => router.replace("/")}
            >
                <Text style={styles.skipText}>Skip for now</Text>
            </PressableScale>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: colors.sand,
        paddingHorizontal: 24,
        paddingTop: 8,
        paddingBottom: 30, // judge by eye.
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
    reminderCard: {
        backgroundColor: colors.surface,
        borderWidth: 1,
        borderColor: colors.border,
        borderRadius: 20,
        paddingVertical: 18,
        paddingHorizontal: 20,
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
    },
    cardTitle: {
        ...type.headline,
        color: colors.ink,
    },
    cardSubtitle: {
        ...type.footnote,
        color: colors.muted,
        marginTop: 2,
    },
    skipButton: {
        alignSelf: "center",
        paddingTop: 16,
    },
    skipText: {
        ...type.subhead,
        color: colors.muted,
    },
    dayRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginTop: 16,
    },
    dayTap: {
        width: 44,
        height: 44,
        alignItems: "center",
        justifyContent: "center",
    },
    dayDot: {
        width: 44,
        height: 44,
        borderRadius: 999,
        borderWidth: 1.5,
        borderColor: colors.border,
        backgroundColor: colors.surface,
        alignItems: "center",
        justifyContent: "center",
    },
    dayDotOn: {
        backgroundColor: colors.sage,
        borderColor: colors.sage,
    },
    dayText: {
        fontFamily: "PlusJakartaSans",
        fontSize: 14,
        fontWeight: "700",
        color: colors.tertiary,
        includeFontPadding: false,
    },
    dayTextOn: {
        color: colors.surface,
    },
    sectionLabel: {
        ...type.footnote,
        fontWeight: "600",
        color: colors.muted,
        marginTop: 24,
        marginBottom: 10,
    },
    presetRow: {
        flexDirection: "row",
        gap: 8,
    },
    pill: {
        flex: 1,
        alignItems: "center",
        borderRadius: 14,
        paddingVertical: 16,
        borderWidth: 1.5,
        borderColor: colors.border,
        backgroundColor: colors.surface,
    },
    pillOn: {
        backgroundColor: colors.sageFill,
        borderColor: colors.sage,
    },
    pillText: {
        fontFamily: "PlusJakartaSans",
        fontSize: 13,
        fontWeight: "700",
        color: colors.muted,
        includeFontPadding: false,
    },
    pillTextOn: {
        color: colors.forest,
    },
    timeList: {
        gap: 8,
    },
    timeCard: {
        height: 56,
        borderRadius: 16,
        backgroundColor: colors.surface,
        borderWidth: 1,
        borderColor: colors.border,
        flexDirection: "row",
        alignItems: "center",
        gap: 6,
        paddingLeft: 16,
        paddingRight: 12,
    },
    timeLabel: {
        flex: 1,
        flexDirection: "row",
        alignItems: "center",
        gap: 10,
    },
    timeText: {
        fontFamily: "PlusJakartaSans",
        fontSize: 16,
        fontWeight: "700",
        color: colors.ink,
        includeFontPadding: false,
    },
    iconTap: {
        width: 44,
        height: 44,
        alignItems: "center",
        justifyContent: "center",
    },
    iconCircle: {
        width: 38,
        height: 38,
        borderRadius: 999,
        alignItems: "center",
        justifyContent: "center",
    },
    editCircle: {
        backgroundColor: colors.sageFill,
    },
    deleteCircle: {
        backgroundColor: colors.destructive,
    },
    addRow: {
        height: 56,
        borderRadius: 16,
        backgroundColor: colors.surface,
        borderWidth: 1,
        borderStyle: "dashed",
        borderColor: colors.faint,
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        gap: 6,
    },
    addRowText: {
        fontFamily: "PlusJakartaSans",
        fontSize: 16,
        fontWeight: "600",
        color: colors.muted,
        includeFontPadding: false,
    },
});
